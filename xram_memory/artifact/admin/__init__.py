from ..models import Document, PDFDocument, ImageDocument
from django.contrib import admin

from xram_memory.artifact.models import Document, PDFDocument, NewsPDFCapture, News
from xram_memory.base_models import TraceableAdminModel

from .models.news import NewsAdmin


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
        'title',
        'teaser',
        'slug',
        'mime_type',
        'file_size',
        'file_hash',
        'additional_info',
        'is_user_object',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
        'is_user_object',
    )
    raw_id_fields = ('keywords', 'subjects')
    search_fields = ('slug',)
    date_hierarchy = 'created_at'


@admin.register(PDFDocument)
class PDFDocumentAdmin(TraceableAdminModel):
    list_display = (
        'id',
        'pdf_file',
        'file_size',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    search_fields = ('title',)
    date_hierarchy = 'modified_at'


@admin.register(ImageDocument)
class ImageDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
        'title',
        'teaser',
        'slug',
        'mime_type',
        'file_size',
        'file_hash',
        'additional_info',
        'is_user_object',
        'image_file',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
        'is_user_object',
    )
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
