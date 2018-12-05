from django.dispatch import receiver
from django.db.models.signals import post_save
from ..archived_news.models import ArchivedNews
from .fetcher import process_news
import logging
import django_rq


logger = logging.getLogger(__name__)


@receiver(post_save, sender=ArchivedNews)
def add_news_archive_to_queue(sender, **kwargs):
    try:
        archived_news = kwargs['instance']
        if (archived_news.status == ArchivedNews.STATUS_NEW):
            logger.info(
                'Notícia com o id {} e status "{}" inserida na fila para processamento.'.format(
                    archived_news.id, archived_news.get_status_display()
                )
            )
            process_news.delay(archived_news)
            # adicione a notícia na fila para  baixar
            # altere o status para 'agendado'
            # salve o modelo
    except:
        pass

    pass
