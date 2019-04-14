from xram_memory.artifact.models import Document, News, Newspaper, NewsPDFCapture, NewsImageCapture
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, Serializer, Field
from xram_memory.taxonomy.serializers import KeywordSerializer, SubjectSerializer
from boltons.cacheutils import cachedproperty
from filer.models import Folder, File


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'description', 'canonical_url',
                  'mime_type', 'size', 'thumbnail', 'thumbnails')


class SimpleDocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'mime_type', 'size',)


class SimpleDocumentSerializerWithThumbnail(ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'mime_type', 'size',
                  'thumbnail', 'thumbnails', 'canonical_url')


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


class PhotoAlbumFolderSerializer(ModelSerializer):
    photos = SimpleDocumentSerializerWithThumbnail(source="files", many=True)

    class Meta:
        model = Folder
        fields = ('id',  'name', 'created_at',
                  'modified_at', 'photos', 'file_count')


class SimplePhotoAlbumFolderSerializer(ModelSerializer):
    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'modified_at', 'file_count')
