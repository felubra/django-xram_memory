from django_rq import job
from newspaper import Article
from ..archived_news.models import ArchivedNews

import logging

logger = logging.getLogger(__name__)


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
    except Exception as error:
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
