from django.contrib import admin

from .models import ArchivedNewsPDFCapture


@admin.register(ArchivedNewsPDFCapture)
class ArchivedNewsPDFCaptureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'size',
        'mime_type',
        'url_of_capture',
        'pdf_file',
        'archived_news',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'archived_news',
    )
    date_hierarchy = 'created_at'
