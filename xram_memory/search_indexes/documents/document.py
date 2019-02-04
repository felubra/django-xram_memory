from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from xram_memory.artifact.models import Document

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={'read_only_allow_delete': False},
    # read_only_allow_delete=False
)


@INDEX.doc_type
class DocumentDocument(DocType):
    id = fields.IntegerField(attr='id')
    # Campos de TraceableModel
    created_at = fields.DateField()
    modified_at = fields.DateField()
    # Campos de TraceableEditorialModel
    published = fields.BooleanField()
    featured = fields.BooleanField()
    # Campos de Artifact
    title = fields.TextField()
    teaser = fields.TextField()
    keywords = fields.KeywordField(
        attr='keywords_indexing',
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    subjects = fields.KeywordField(
        attr='subjects_indexing',
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )
    # Campos de Document
    mime_type = fields.KeywordField()
    file_size = fields.IntegerField()
    file = fields.KeywordField(
        attr='file_indexing',
    )

    class Meta(object):
        model = Document  # O modelo associado a este documento
        parallel_indexing = True
