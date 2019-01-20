from django.contrib import admin

from xram_memory.artifact.models import Document, PDFDocument, NewsPDFCapture, News
from xram_memory.base_models import TraceableAdminModel

from .models.news import NewsAdmin


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
