from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Keyword
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(
    hosts=['127.0.0.1'])  # @todo, usar uma config


class ArchivedNewsIndex(Document):
    url = Text()
    archived_news_url = Text()
    title = Text()
    summary = Text()
    text = Text()
    created_at = Date()
    modified_at = Date()

    authors = Keyword(multiple=True)
    keywords = Keyword(multiple=True)

    class Index:
        index = 'archived_news-index'
        name = 'archived_news-index'

    def save(self, ** kwargs):
        # transforme os campos abaixo numa string com separação por vírgula
        self.authors = self.authors.split(",")
        self.keywords = [keyword.name for keyword in self.keywords.all()]
        return super(ArchivedNewsIndex, self).save(** kwargs)


def bulk_indexing():
    ArchivedNewsIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
                             for b in models.ArchivedNews.objects.all().iterator()))
