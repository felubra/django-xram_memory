from rest_framework.serializers import ModelSerializer, CharField, IntegerField, Serializer, Field, SerializerMethodField
from xram_memory.artifact.models import Document, News, Newspaper, NewsPDFCapture, NewsImageCapture
from xram_memory.taxonomy.serializers import KeywordSerializer, SubjectSerializer
from hashid_field.rest import HashidSerializerCharField, Hashid
from boltons.cacheutils import cachedproperty
from filer.models import Folder, File
from django.conf import settings


class ArtifactSerializer(Serializer):
    slug = SerializerMethodField()
    thumbnail = SerializerMethodField()
    title = SerializerMethodField()
    description = SerializerMethodField()
    type = SerializerMethodField()


    def get_slug(self, obj):
        if isinstance(obj, News):
            return obj.slug
        elif isinstance(obj, Document):
            return obj.document_id_indexing
        else:
            raise NotImplementedError('Tipo de modelo não suportado')

    def get_type(self, obj):
        if isinstance(obj, News):
            return 'news'
        elif isinstance(obj, Document):
            return 'document'
        else:
            raise NotImplementedError('Tipo de modelo não suportado')

    def get_thumbnail(self, obj):
        if isinstance(obj, News):
            return obj.thumbnail
        elif isinstance(obj, Document):
            return obj.search_thumbnail
        else:
            raise NotImplementedError('Tipo de modelo não suportado')

    def get_title(self, obj):
        if isinstance(obj, News):
            return obj.title
        elif isinstance(obj, Document):
            return obj.name
        else:
            raise NotImplementedError('Tipo de modelo não suportado')

    def get_description(self, obj):
        if isinstance(obj, News):
            return obj.teaser
        elif isinstance(obj, Document):
            return obj.description
        else:
            raise NotImplementedError('Tipo de modelo não suportado')


class NewspaperSerializer(ModelSerializer):
    class Meta:
        model = Newspaper
        fields = ('title', 'description', 'favicon_logo',
                  'url', 'modified_at', 'created_at')


class SimpleNewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'slug', 'thumbnail', 'modified_at', 'created_at')
    thumbnail = CharField()


class DocumentSerializer(ModelSerializer):
    document_id = HashidSerializerCharField(
        source_field='artifact.Document.document_id')

    class Meta:
        model = Document
        fields = ('document_id', 'name', 'description', 'canonical_url', 'uploaded_at',
                  'modified_at', 'mime_type', 'size', 'thumbnail', 'thumbnails', 'news_items')

    news_items = SimpleNewsSerializer(source='related_news', many=True)


class SimpleDocumentSerializer(ModelSerializer):
    document_id = HashidSerializerCharField(
        source_field='artifact.Document.document_id')

    class Meta:
        model = Document
        fields = ('document_id', 'name', 'mime_type', 'size', 'modified_at',
                  'uploaded_at',)


class SimpleDocumentSerializerWithThumbnail(ModelSerializer):
    document_id = HashidSerializerCharField(
        source_field='artifact.Document.document_id')

    class Meta:
        model = Document
        fields = ('document_id', 'name', 'mime_type', 'size',
                  'thumbnail', 'thumbnails', 'canonical_url', 'uploaded_at',
                  'modified_at',)


class PDFCaptureSerializer(ModelSerializer):
    class Meta:
        model = NewsPDFCapture
        fields = ('pdf_document', 'pdf_capture_date',)
    pdf_document = SimpleDocumentSerializer()

class ImageCaptureSerializer(ModelSerializer):
    class Meta:
        model = NewsImageCapture
        fields = ('image_document', 'image_capture_date',)
    image_document = SimpleDocumentSerializer()

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'teaser', 'slug',
                  'url', 'archived_news_url', 'authors', 'body', 'published_date', 'language',
                  'newspaper', 'keywords', 'subjects', 'pdf_captures', 'image_capture',
                  'thumbnail', 'thumbnails', 'modified_at', 'created_at',)
    newspaper = NewspaperSerializer()
    keywords = KeywordSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    pdf_captures = PDFCaptureSerializer(many=True)
    image_capture = ImageCaptureSerializer()
    thumbnail = CharField()


class PhotoAlbumFolderSerializer(ModelSerializer):
    photos = DocumentSerializer(source="files", many=True)
    album_id = SerializerMethodField()
    cover = SerializerMethodField()
    big_cover = SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('album_id',  'name', 'created_at',
                  'modified_at', 'photos', 'file_count', 'cover', 'big_cover')

    def get_album_id(self, obj):
        hashid = Hashid(obj.pk, settings.HASHID_FIELD_SALT, 7)
        return hashid.hashid

    def get_cover(self, obj):
        try:
            return (obj.files
                .filter(is_public=True)
                .order_by('-modified_at')
                    [0].thumbnail
            )
        except Exception as e:
            return ''

    def get_big_cover(self, obj):
        try:
            return (obj.files
                .filter(is_public=True)
                .order_by('-modified_at')
                    [0].thumbnails['1280']
            )
        except Exception as e:
            return ''


class SimplePhotoAlbumFolderSerializer(PhotoAlbumFolderSerializer):
    class Meta:
        model = Folder
        fields = ('album_id', 'name', 'created_at',
                  'modified_at', 'file_count', 'cover', 'big_cover')
