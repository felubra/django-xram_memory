from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(
    hosts=['192.168.99.100'])  # @todo, usar uma config


class ArchivedNewsIndex(Document):
    url = Text()
    title = Text()
    summary = Text()

    class Index:
        index = 'archived_news-index'
        name = 'archived_news-index'


def bulk_indexing():
    ArchivedNewsIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
                             for b in models.ArchivedNews.objects.all().iterator()))
