from xram_memory.artifact.models import Document, NewsImageCapture, NewsPDFCapture
from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl.serializer import AttrJSONSerializer
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.taxonomy.models import Keyword, Subject
from django.conf import settings
from hashid_field import Hashid

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
class DocumentDocument(DocType):
    """
    Índice de pesquisa para o modelo Document
    """
    # Campos comuns
    id = fields.IntegerField(attr='id')
    created_at = fields.DateField(attr="uploaded_at")
    modified_at = fields.DateField(attr="modified_at")
    title = fields.TextField(analyzer='rebuilt_portuguese', attr="name")
    teaser = fields.TextField(
        analyzer='rebuilt_portuguese', attr="description")
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
    # Campos específicos de Document
    document_id = fields.KeywordField(attr='document_id_indexing')
    mime_type = fields.KeywordField()

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Keyword):
            return related_instance.document.all()
        elif isinstance(related_instance, Subject):
            return related_instance.document.all()
        elif isinstance(related_instance, NewsImageCapture):
            return related_instance.image_document
        elif isinstance(related_instance, NewsPDFCapture):
            return related_instance.pdf_document

    def get_queryset(self):
        """
        Somente indexe documentos que tiverem document_id, forem inseridos pelo usuário e públicos.
        """
        return self._doc_type.model._default_manager.filter(document_id__isnull=False).filter(is_user_object=True).filter(is_public=True)

    class Meta(object):
        model = Document  # O modelo associado a este documento
        parallel_indexing = True
        doc_type = 'Documento'
        related_models = [Keyword, Subject,
                          NewsPDFCapture, NewsImageCapture]
