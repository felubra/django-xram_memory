from .models import ArchivedNews
from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch.exceptions import ConnectionError


@receiver(post_save, sender=ArchivedNews)
def index_post(sender, **kwargs):
    archived_news = kwargs['instance']
    if not archived_news:
        return
    # @todo: verificar porque não posso fazer o tratamento de exceção aqui

    archived_news.indexing()
