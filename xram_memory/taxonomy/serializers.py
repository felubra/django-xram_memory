from rest_framework.serializers import ModelSerializer
from xram_memory.taxonomy.models import Keyword, Subject

TAXONOMY_ITEM_FIELDS = fields = ('slug', 'name',)


class KeywordSerializer(ModelSerializer):
    class Meta:
        model = Keyword
        fields = TAXONOMY_ITEM_FIELDS
        depth = 1


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = TAXONOMY_ITEM_FIELDS + \
            ('description', 'cover', 'big_cover', 'items_count',)
        depth = 1


class SimpleSubjectSerializer(SubjectSerializer):
    class Meta:
        model = Subject
        fields = TAXONOMY_ITEM_FIELDS + \
            ('items_count',)
        depth = 1
