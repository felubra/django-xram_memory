from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from xram_memory.artifact.models import News, NewsPDFCapture, NewsImageCapture
from xram_memory.taxonomy.models import Keyword, Subject

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    blocks={'read_only_allow_delete': False},
    analysis={
        "filter": {
            "portuguese_stop": {
                "type":       "stop",
                "stopwords":  "_portuguese_"
            },
            "portuguese_stemmer": {
                "type":       "stemmer",
                "language":   "light_portuguese"
            },
            "snowball_portuguese": {
                "type": "snowball",
                "language":   "portuguese"
            }
        },
        'analyzer': {
            "rebuilt_portuguese": {
                "tokenizer":  "standard",
                "filter": [
                    "lowercase",
                    "portuguese_stop",
                    "portuguese_stemmer"
                ]
            },
            'html_strip': {
                'tokenizer': "standard",
                'filter': ["standard", "lowercase", "stop", "snowball"],
                'char_filter': ["html_strip"]
            },
        },
        "normalizer": {
            "my_normalizer": {
                "type": "custom",
                "char_filter": [],
                "filter": ["lowercase", "asciifolding"]
            }
        }

    }
)


@INDEX.doc_type
class NewsImageCaptureDocument(DocType):
    """
    Índice de pesquisa para o modelo NewsImageCapture
    """
    # Campos comuns
    # TODO: NÃO ESTÁ EVITANDO COLISÕES
    id = fields.IntegerField(attr='indexed_id')
    created_at = fields.DateField(attr="image_capture_date")
    modified_at = fields.DateField(attr="image_capture_date")
    title = fields.TextField(
        analyzer='rebuilt_portuguese', attr="__str__")  # TODO
    teaser = fields.TextField(
        analyzer='rebuilt_portuguese', attr="__str__")
    keywords = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    subjects = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    thumbnail = fields.KeywordField(
        attr='search_thumbnail'
    )
    published_year = fields.IntegerField(attr="published_year")
    indexed_type = fields.KeywordField(attr="indexed_type")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Keyword):
            return related_instance.news.all()
        elif isinstance(related_instance, Subject):
            return related_instance.news.all()
        elif isinstance(related_instance, News):
            return related_instance.news.all()

    class Meta(object):
        model = NewsImageCapture  # O modelo associado a este documento
        parallel_indexing = True
        doc_type = 'Captura de notícia'
        related_models = [Keyword, Subject,
                          News]


@INDEX.doc_type
class NewsPDFCaptureDocument(DocType):
    """
    Índice de pesquisa para o modelo NewsPDFCapture
    """
    # Campos comuns
    # TODO: NÃO ESTÁ EVITANDO COLISÕES
    id = fields.IntegerField(attr='indexed_id')
    created_at = fields.DateField(attr="pdf_capture_date")
    modified_at = fields.DateField(attr="pdf_capture_date")
    title = fields.TextField(
        analyzer='rebuilt_portuguese', attr="__str__")  # TODO
    teaser = fields.TextField(
        analyzer='rebuilt_portuguese', attr="__str__")
    keywords = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    subjects = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    thumbnail = fields.KeywordField(
        attr='search_thumbnail'
    )
    published_year = fields.IntegerField(attr="published_year")
    indexed_type = fields.KeywordField(attr="indexed_type")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Keyword):
            return related_instance.news.all()
        elif isinstance(related_instance, Subject):
            return related_instance.news.all()
        elif isinstance(related_instance, News):
            return related_instance.news.all()

    class Meta(object):
        model = NewsPDFCapture  # O modelo associado a este documento
        parallel_indexing = True
        doc_type = 'Captura de notícia'
        related_models = [Keyword, Subject,
                          News]
