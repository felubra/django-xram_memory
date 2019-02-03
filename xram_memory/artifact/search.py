from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Keyword
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models
from django.conf import settings

connections.create_connection(
    hosts=settings.ELASTIC_SEARCH_HOSTS)


class NewsIndex(Document):
    title = Text()
    teaser = Text()
    body = Text()
    published_date = Date()
    language = Text()

    keywords = Keyword(multi=True)
    subjects = Keyword(multi=True)

    class Index:
        index = 'news-index'
        name = 'news-index'

    def save(self, ** kwargs):
        # transforme os campos abaixo numa string com separação por vírgula
        self.keywords = [keyword.name for keyword in self.keywords.all()]
        self.subjects = [subject.name for subject in self.subjects.all()]
        return super(NewsIndex, self).save(** kwargs)


def bulk_indexing():
    NewsIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
                             for b in models.News.objects.all().iterator()))
