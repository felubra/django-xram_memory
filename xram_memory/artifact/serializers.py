from filer.models import File
from rest_framework.serializers import ModelSerializer, CharField
from xram_memory.artifact.models import News, Newspaper, NewsPDFCapture, NewsImageCapture
from xram_memory.taxonomy.serializers import KeywordSerializer, SubjectSerializer


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'description',
                  'canonical_url', 'size',)


class SimpleDocumentSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'canonical_url', 'size',)


class PDFCaptureSerializer(ModelSerializer):
    class Meta:
        model = NewsPDFCapture
        fields = ('pdf_document', 'pdf_capture_date',)
    pdf_document = SimpleDocumentSerializer()


class NewspaperSerializer(ModelSerializer):
    class Meta:
        model = Newspaper
        fields = ('title', 'slug',
                  'description', 'logo', 'url')


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'teaser', 'slug',
                  'url', 'archived_news_url', 'authors', 'body', 'published_date', 'language', 'newspaper', 'keywords',
                  'subjects', 'pdf_captures', 'image_capture', 'thumbnail')
    newspaper = NewspaperSerializer()
    keywords = KeywordSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    pdf_captures = PDFCaptureSerializer(many=True)
    image_capture = CharField(source='image_capture_indexing')
    thumbnail = CharField()
