import os
import datetime
import pdfkit
import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from newspaper import Article
from goose3 import Goose
from goose3.image import Image
from django_rq import job
from pathlib import Path
from timeit import default_timer
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType

from ..archived_news.models import ArchivedNews
from ..documents.models import ArchivedNewsPDFCapture
from .signals import (basic_info_started, basic_info_acquired, basic_info_failed,
                      internet_archive_started, internet_archive_acquired, internet_archive_failed,
                      pdf_capture_started, pdf_capture_acquired, pdf_capture_failed)

saved_pdf_dir = os.path.join(
    settings.MEDIA_ROOT, settings.NEWS_FETCHER_SAVED_DIR_PDF)


@job
def archive_org_fetcher(ArchivedNews):
    pass


def verify_if_in_archive_org(archived_news: ArchivedNews):
    try:

        internet_archive_started.send_robust(
            sender=None, archived_news=archived_news)

        tic = default_timer()
        response = requests.get(
            "https://archive.org/wayback/available?url={}".format(archived_news.url))
        response.raise_for_status()
        response = response.json()
        toc = default_timer()
        if (response["archived_snapshots"] and response["archived_snapshots"]["closest"] and
                response["archived_snapshots"]["closest"]["available"]):
            closest_archive = response["archived_snapshots"]["closest"]
            archived_news.archived_news_url = closest_archive["url"]

    except Exception as err:

        internet_archive_failed.send_robust(
            sender=None, archived_news=archived_news, error_message=str(err))

    else:

        internet_archive_acquired.send_robust(
            sender=None, archived_news=archived_news, time_took=toc - tic)

        archived_news.force_archive_org_processing = False
        archived_news.status = ArchivedNews.STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED
        # TODO:: salvar a entrada do log noutro lugar
        '''LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionada versão encontrada no Archive.org.")'''


def _extract_using_newspaper(url, raw_html=None):
    '''
    Tenta extrair usando a biblioteca newspaper3k
    '''
    try:
        newspaper_article = Article(url)

        if raw_html:
            newspaper_article.download(input_html=raw_html)
        else:
            newspaper_article.download()
        newspaper_article.parse()
        newspaper_article.nlp()

        return newspaper_article
    except:
        return None


def _extract_using_goose3(url, raw_html=None):
    '''
    Tenta extrair usando a biblioteca goose3
    '''
    try:
        goose = Goose({'enable_image_fetching': True})

        if raw_html:
            goose_article = goose.extract(raw_html=raw_html, url=url)
        else:
            goose_article = goose.extract(url=url)

        return goose_article
    except:
        return None


def archived_news_extract_basic_info(url):
    '''
    Retorna uma tupla com as extrações de informações básicas para determinada url de Notícia Arquivada.
    '''
    # Tente extrair primeiro usando o newspaper3k e reutilize seu html, se possível
    newspaper_article = _extract_using_newspaper(url)
    if newspaper_article:
        goose_article = _extract_using_goose3(
            url, newspaper_article.html)
    else:
        goose_article = _extract_using_goose3(url)
    if newspaper_article is None and goose_article is None:
        raise(Exception(
            'Não foi possível extrair informações básicas sobre a notícia, pois nenhum dos extratores funcionou.'))
    return (newspaper_article, goose_article,)


def _merge_extractions(newspaper_article, goose_article):
    '''
    Com base nas extrações passadas, constrói um dicionário em que a informação de cada uma é aproveitada, se existir.
    '''
    def join_with_comma(list):
        return ",".join(list)

    try:
        # TODO: melhorar esse código, que está safo, mas feio pra caramba
        archived_news_dict = {
            'title': newspaper_article.title if getattr(newspaper_article, 'title', None) else getattr(goose_article, 'title', None),
            'top_image': newspaper_article.top_image if getattr(newspaper_article, 'top_image', None) else goose_article.top_image.src if isinstance(getattr(goose_article, 'top_image', None), Image) else None,
            'text': newspaper_article.text if getattr(newspaper_article, 'text', None) else getattr(goose_article, 'cleaned_text', None),
            'summary': getattr(newspaper_article, 'summary', None),

            'published_date': newspaper_article.publish_date if getattr(newspaper_article, 'publish_date', None) else getattr(goose_article, 'publish_date', None),

            'authors': join_with_comma(newspaper_article.authors if getattr(newspaper_article, 'authors', []) else getattr(goose_article, 'authors', [])),
            'images': join_with_comma(getattr(newspaper_article, 'images', [])),
            'keywords': newspaper_article.keywords if getattr(newspaper_article, 'keywords', []) else getattr(goose_article, 'tags', []),
        }
        return archived_news_dict
    except Exception as err:
        raise(
            Exception(
                "Falha ao construir o dicionário com as informações básicas da notícia arquivada: {}."
                .format(str(err))
            )
        )


def extract_basic_info(archived_news):
    newspaper_article, goose_article = archived_news_extract_basic_info(
        archived_news.url)
    return _merge_extractions(newspaper_article, goose_article)


@job
def process_news(archived_news: ArchivedNews):
    try:

        basic_info_started.send_robust(
            sender=None, archived_news=archived_news)

        archived_news.status = ArchivedNews.STATUS_QUEUED_BASIC_INFO
        tic = default_timer()
        archived_news_dict = extract_basic_info(archived_news)
        toc = default_timer()

        for prop, value in archived_news_dict.items():
            if prop == 'keywords':
                setattr(archived_news, '_keywords', value)
            else:
                setattr(archived_news, prop, value)

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_PROCESS
        finally:
            basic_info_failed.send_robust(
                sender=None, archived_news=archived_news, error_message=str(err))

    else:

        basic_info_acquired.send_robust(
            sender=None, archived_news=archived_news, time_took=toc-tic)

        archived_news.force_basic_processing = False
        status_before = archived_news.get_status_display()
        archived_news.status = ArchivedNews.STATUS_PROCESSED_BASIC_INFO
        # TODO:: tratar casos de edição e adição separadamente
        # TODO:: salvar a entrada do log noutro lugar
        '''LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionadas informações básicas da notícia obtidas automaticamente.")'''


def get_pdf_capture(archived_news: ArchivedNews):
    try:

        pdf_capture_started.send_robust(
            sender=None, archived_news=archived_news)

        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        if not saved_pdf_dir:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração NEWS_FETCHER_SAVED_DIR_PDF).')

        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )

        archived_news_pdf_path = str(
            Path(saved_pdf_dir, uniq_filename))

        # TODO: usar um decorador para medir o tempo e logar
        tic = default_timer()
        pdfkit.from_url(archived_news.url, archived_news_pdf_path, options={
            'print-media-type': None,
            'disable-javascript': None,
        })
        toc = default_timer()

        pdf_capture = ArchivedNewsPDFCapture(url_of_capture=archived_news.url,
                                             pdf_file=archived_news_pdf_path,
                                             archived_news=archived_news)

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_CAPTURE
        finally:
            pdf_capture_failed.send_robust(
                sender=None, archived_news=archived_news, error_message=str(err))

    finally:

        return pdf_capture


def save_news_as_pdf(archived_news: ArchivedNews):
    try:

        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        if not saved_pdf_dir:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração NEWS_FETCHER_SAVED_DIR_PDF).')

        pdf_capture_started.send_robust(
            sender=None, archived_news=archived_news)

        archived_news.status = ArchivedNews.STATUS_QUEUED_PAGE_CAPTURE

        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )

        archived_news_pdf_path = str(
            Path(saved_pdf_dir, uniq_filename))

        # TODO: usar um decorador para medir o tempo e logar
        tic = default_timer()
        pdfkit.from_url(archived_news.url, archived_news_pdf_path, options={
            'print-media-type': None,
            'disable-javascript': None,
        })
        toc = default_timer()

        pdf_capture = ArchivedNewsPDFCapture.objects.create(url_of_capture=archived_news.url,
                                                            pdf_file=archived_news_pdf_path,
                                                            archived_news=archived_news)
        # TODO:: tratar casos de edição e adição separadamente
        # TODO:: salvar a entrada do log noutro lugar
        '''LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                pdf_capture).pk,
            object_id=pdf_capture.id,
            object_repr=repr(pdf_capture),
            action_flag=ADDITION,
            change_message="Adicionado um documento de captura para a notícia arquivada com o id {}.".format(archived_news.pk))'''

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_CAPTURE
        finally:
            pdf_capture_failed.send_robust(
                sender=None, archived_news=archived_news, error_message=str(err))

    else:

        pdf_capture_acquired.send_robust(
            sender=None, archived_news=archived_news, time_took=toc-tic, pdf_capture=pdf_capture)

        archived_news.force_pdf_capture = False
        archived_news.status = ArchivedNews.STATUS_PROCESSED_PAGE_CAPTURE
        # TODO:: salvar a entrada do log noutro lugar
        # TODO:: tratar casos de edição e adição separadamente
        '''LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionado documento de captura de página com o ID {}".format(archived_news.id))'''


@job
def save_news_as_pdf_job(archived_news: ArchivedNews):
    try:
        save_news_as_pdf(archived_news)
    finally:
        archived_news.save()


@job
def process_news_job(archived_news: ArchivedNews):
    try:
        process_news(archived_news)
    finally:
        archived_news.save()


@job
def verify_if_in_archive_org_job(archived_news: ArchivedNews):
    try:
        verify_if_in_archive_org(archived_news)
    finally:
        archived_news.save()
