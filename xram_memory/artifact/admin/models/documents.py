from django.contrib import admin
from xram_memory.artifact.models import Document, PDFDocument, ImageDocument
from ..forms.documents import PDFDocumentAdminForm, ImageDocumentAdminForm
from xram_memory.base_models import TraceableAdminModel


@admin.register(Document)
class DocumentAdmin(TraceableAdminModel):
    list_display = (
        'id',
        'file',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'mime_type',
        'file_size',
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
        'file',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'mime_type',
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
    form = PDFDocumentAdminForm


@admin.register(ImageDocument)
class ImageDocumentAdmin(TraceableAdminModel):
    list_display = (
        'id',
        'file',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'mime_type',
        'file_size',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
    form = ImageDocumentAdminForm
