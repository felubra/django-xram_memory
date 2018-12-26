import os
import datetime
import pdfkit
import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from newspaper import Article
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


@job
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
        archived_news.save()
        # @todo: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionada versão encontrada no Archive.org.")


@job
def process_news(archived_news: ArchivedNews):
    try:

        basic_info_started.send_robust(
            sender=None, archived_news=archived_news)

        archived_news.status = ArchivedNews.STATUS_QUEUED_BASIC_INFO
        archived_news.save()

        tic = default_timer()
        article = Article(archived_news.url)
        article.download()
        article.parse()
        article.nlp()
        toc = default_timer()
        updateable_fields = ('title', 'authors', 'keywords',
                             'images', 'top_image', 'text', 'summary',)
        multiple_value_fields = ('images', 'authors', 'keywords',)

        # @todo: baixar images e top_image
        for field in updateable_fields:
            value = getattr(article, field, None)
            if value:
                if field in multiple_value_fields:
                    if field == 'keywords':
                        setattr(archived_news, '_keywords', ",".join(value))
                    else:
                        setattr(archived_news, field, ",".join(value))
                else:
                    setattr(archived_news, field, value)

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_PROCESS
            archived_news.save()
        finally:
            basic_info_failed.send_robust(
                sender=None, archived_news=archived_news, error_message=str(err))

    else:

        basic_info_acquired.send_robust(
            sender=None, archived_news=archived_news, time_took=toc-tic)

        archived_news.force_basic_processing = False
        status_before = archived_news.get_status_display()
        archived_news.status = ArchivedNews.STATUS_PROCESSED_BASIC_INFO
        archived_news.save()

        # @todo: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionadas informações básicas da notícia obtidas automaticamente.")


@job
def save_news_as_pdf(archived_news: ArchivedNews):
    try:

        # @todo checar se o diretório existe, se existem permissões para salvar etc
        if not saved_pdf_dir:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração NEWS_FETCHER_SAVED_DIR_PDF).')

        pdf_capture_started.send_robust(
            sender=None, archived_news=archived_news)

        archived_news.status = ArchivedNews.STATUS_QUEUED_PAGE_CAPTURE
        archived_news.save()

        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )

        archived_news_pdf_path = str(
            Path(saved_pdf_dir, uniq_filename))

        # @todo usar um decorador para medir o tempo e logar
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
            archived_news.save()
        finally:
            pdf_capture_failed.send_robust(
                sender=None, archived_news=archived_news, error_message=str(err))

    else:

        pdf_capture_acquired.send_robust(
            sender=None, archived_news=archived_news, time_took=toc-tic, pdf_capture=pdf_capture)

        archived_news.force_pdf_capture = False
        archived_news.status = ArchivedNews.STATUS_PROCESSED_PAGE_CAPTURE
        archived_news.save()
        # @todo: tratar casos de edição e adição separadamente
        LogEntry.objects.log_action(
            user_id=archived_news.modified_by_id,
            content_type_id=ContentType.objects.get_for_model(
                archived_news).pk,
            object_id=archived_news.id,
            object_repr=repr(archived_news),
            action_flag=CHANGE,
            change_message="Adicionado documento de captura de página com o ID {}".format(archived_news.id))
