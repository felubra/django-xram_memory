from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from xram_memory.artifact.models import News, NewsPDFCapture
from xram_memory.taxonomy.models import Keyword, Subject

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={'read_only_allow_delete': False},
    # read_only_allow_delete=False
)


@INDEX.doc_type
class NewsDocument(DocType):
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
    keywords = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    subjects = fields.NestedField(properties={
        'name': fields.KeywordField(),
        'slug': fields.KeywordField()
    })
    # Campos de News
    published_date = fields.DateField()
    language = fields.KeywordField()

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Keyword):
            return related_instance.news.all()
        elif isinstance(related_instance, Subject):
            return related_instance.news.all()

    class Meta(object):
        model = News  # O modelo associado a este documento
        parallel_indexing = True
        related_models = [Keyword, Subject, NewsPDFCapture]
