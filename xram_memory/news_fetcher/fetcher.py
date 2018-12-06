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
        article = Article(archived_news.url)
        article.download()
        article.parse()
        article.nlp()

        archived_news.title = article.title
        archived_news.authors = ",".join(article.authors)
        archived_news.keywords = ",".join(article.keywords)
        archived_news.images = ",".join(article.images)
        archived_news.text = article.text
        archived_news.summary = article.summary
        archived_news.status = ArchivedNews.STATUS_PROCESSED
        archived_news.save()
        logger.info(
            'Sucesso ao processar Notícia com o id {} e status "{}".'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )
    except:
        logger.error(
            'Falha ao processar Notícia com o id {} e status "{}".'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )
        try:
            archived_news.status = ArchivedNews.STATUS_ERROR
            archived_news.save()
        except:
            pass


@job
def save_news_as_pdf(archived_news):
    try:
        uniq_filename = str(datetime.datetime.now().date(
        )) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'

        archived_news_pdf_path = str(
            Path(saved_pages_dir, uniq_filename))

        # @todo usar um decorador para medir o tempo e logar
        tic = default_timer()
        pdfkit.from_url(archived_news.url, archived_news_pdf_path, options={
            'print-media-type': None,
            'disable-javascript': None
        })
        toc = default_timer()

        logger.info(
            'Notícia com o id {} salva em formato PDF "{}" em {}s.'.format(
                archived_news.id, archived_news_pdf_path, toc - tic
            )
        )
    except:
        logger.error(
            'Falha ao tentar salvar a Notícia em formato PDF com o id {} e status "{}".'.format(
                archived_news.id, archived_news.get_status_display()
            )
        )
        try:
            archived_news.status = ArchivedNews.STATUS_ERROR_NO_CAPTURE
            archived_news.save()
        except:
            pass
