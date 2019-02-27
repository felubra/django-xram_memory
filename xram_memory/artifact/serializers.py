from rest_framework.serializers import ModelSerializer
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.taxonomy.serializers import KeywordSerializer, SubjectSerializer


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'teaser', 'slug',
                  'mime_type', 'file_size', 'file',)


class NewspaperSerializer(ModelSerializer):
    class Meta:
        model = Newspaper
        fields = ('title', 'slug',
                  'description', 'logo',)


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'teaser', 'slug',
                  'url', 'archived_news_url', 'authors', 'body', 'published_date', 'language', 'newspaper', 'keywords',
                  'subjects',)
    newspaper = NewspaperSerializer()
    keywords = KeywordSerializer(many=True)
    subjects = SubjectSerializer(many=True)
