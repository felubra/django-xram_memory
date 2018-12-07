import logging
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ..archived_news.models import ArchivedNews
from newspaper import Article
from django_rq import job
from pathlib import Path
import datetime
import pdfkit
from timeit import default_timer


logger = logging.getLogger(__name__)
saved_pages_dir = settings.NEWS_FETCHER_STATIC_DIR


@job
def process_news(archived_news):
    try:

        archived_news.status = ArchivedNews.STATUS_QUEUED_BASIC_INFO
        archived_news.save()
        logger.info(
            'Notícia com o id {} e status "{}" inserida na fila para processamento básico.'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )

        article = Article(archived_news.url)
        article.download()
        article.parse()
        article.nlp()

        archived_news.title = article.title
        archived_news.authors = ",".join(article.authors)
        archived_news.keywords = ",".join(article.keywords)
        archived_news.images = ",".join(article.images)
        archived_news.top_image = article.top_image
        archived_news.text = article.text
        archived_news.summary = article.summary

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_PROCESS
            archived_news.save()
        finally:
            logger.error(
                'Falha ao processar Notícia com o id {} e status "{}": {}'.format(
                    archived_news.id, archived_news.get_status_display(), str(err)
                )
            )

    else:

        status_before = archived_news.get_status_display()
        archived_news.status = ArchivedNews.STATUS_PROCESSED_BASIC_INFO
        archived_news.save()
        logger.info(
            'Sucesso ao processar Notícia com o id {} e status "{}".'.format(
                archived_news.id, status_before
            )
        )


@job
def save_news_as_pdf(archived_news):
    try:

        if not saved_pages_dir:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração NEWS_FETCHER_STATIC_DIR).')

        archived_news.status = ArchivedNews.STATUS_QUEUED_PAGE_CAPTURE
        archived_news.save()
        logger.info(
            'Notícia com o id {} e status "{}" inserida na fila para captura de página.'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )

        uniq_filename = str(datetime.datetime.now().date(
        )) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'

        archived_news_pdf_path = str(
            Path(saved_pages_dir, uniq_filename))

        # @todo usar um decorador para medir o tempo e logar
        tic = default_timer()
        pdfkit.from_url(archived_news.url, archived_news_pdf_path, options={
            'print-media-type': None,
            'disable-javascript': None,
        })
        toc = default_timer()

    except Exception as err:

        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_CAPTURE
            archived_news.save()
        finally:
            logger.error(
                'Falha ao tentar salvar a Notícia em formato PDF com o id {} e status "{}".'.format(
                    archived_news.id, archived_news.get_status_display()
                )
            )

    else:

        archived_news.status = ArchivedNews.STATUS_PROCESSED_PAGE_CAPTURE
        archived_news.save()
        logger.info(
            'Notícia com o id {} salva em formato PDF "{}" em {}s.'.format(
                archived_news.id, archived_news_pdf_path, toc - tic
            )
        )
