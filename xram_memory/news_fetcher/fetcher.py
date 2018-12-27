import os
import datetime
import logging

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

logger = logging.getLogger(__name__)
saved_pdf_dir = os.path.join(
    settings.MEDIA_ROOT, settings.NEWS_FETCHER_SAVED_DIR_PDF)


@job
def archive_org_fetcher(ArchivedNews):
    pass


def verify_if_in_archive_org(archived_news: ArchivedNews):
    try:

        response = requests.get(
            "https://archive.org/wayback/available?url={}".format(archived_news.url))
        response.raise_for_status()
        response = response.json()
        if (response["archived_snapshots"] and response["archived_snapshots"]["closest"] and
                response["archived_snapshots"]["closest"]["available"]):
            closest_archive = response["archived_snapshots"]["closest"]
            archived_news.archived_news_url = closest_archive["url"]

    except Exception as err:

        logger.error(
            'Falha ao tentar localizar uma versão arquivada no Internet Archive para a Notícia com o id {} e status "{}": {}'.format(
                archived_news.id, archived_news.get_status_display(), str(err)
            )
        )
        raise(err)

    else:

        archived_news.force_archive_org_processing = False
        status_before = archived_news.get_status_display()
        archived_news.status = ArchivedNews.STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED
        archived_news.save()
        # TODO:: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionada versão encontrada no Archive.org.")
        logger.info(
            'Sucesso ao pegar informações da Notícia com o id {} e status "{} no Internet Archive".'.format(
                archived_news.id, status_before
            )
        )


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
            '_keywords': newspaper_article.keywords if getattr(newspaper_article, 'keywords', []) else getattr(goose_article, 'tags', []),
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

        archived_news.status = ArchivedNews.STATUS_QUEUED_BASIC_INFO
        logger.info(
            'Notícia com o id {} e status "{}" inserida na fila para processamento básico.'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )

        archived_news_dict = extract_basic_info(archived_news)

        for prop, value in archived_news_dict.items():
            setattr(archived_news, prop, value)

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_PROCESS
        finally:
            logger.error(
                'Falha ao processar Notícia com o id {} e status "{}": {}'.format(
                    archived_news.id, archived_news.get_status_display(), str(err)
                )
            )
            raise(err)

    else:
        archived_news.force_basic_processing = False
        status_before = archived_news.get_status_display()
        archived_news.status = ArchivedNews.STATUS_PROCESSED_BASIC_INFO
        archived_news.save()
        # TODO:: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionadas informações básicas da notícia obtidas automaticamente.")
        logger.info(
            'Sucesso ao processar Notícia com o id {} e status "{}".'.format(
                archived_news.id, status_before
            )
        )


def save_news_as_pdf(archived_news: ArchivedNews):
    try:

        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        if not saved_pdf_dir:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração NEWS_FETCHER_SAVED_DIR_PDF).')

        archived_news.status = ArchivedNews.STATUS_QUEUED_PAGE_CAPTURE
        logger.info(
            'Notícia com o id {} e status "{}" inserida na fila para captura de página.'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )

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
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                pdf_capture).pk,
            object_id=pdf_capture.id,
            object_repr=repr(pdf_capture),
            action_flag=ADDITION,
            change_message="Adicionado um documento de captura para a notícia arquivada com o id {}.".format(archived_news.pk))

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_CAPTURE
        finally:
            logger.error(
                'Falha ao tentar salvar a Notícia em formato PDF com o id {} e status "{}".'.format(
                    archived_news.id, archived_news.get_status_display()
                )
            )
            raise(err)

    else:

        archived_news.force_pdf_capture = False
        archived_news.status = ArchivedNews.STATUS_PROCESSED_PAGE_CAPTURE
        archived_news.save()
        # TODO:: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionado documento de captura de página com o ID {}".format(archived_news.id))
        logger.info(
            'Notícia com o id {} salva em formato PDF "{}" em {}s.'.format(
                archived_news.id, archived_news_pdf_path, toc - tic
            )
        )


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
