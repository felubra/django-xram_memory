from django.contrib import admin

from .models import PDFFile


@admin.register(PDFFile)
class PDFFileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'filename',
    )
    list_filter = ('created_by', 'modified_by', 'created_at', 'modified_at')
    date_hierarchy = 'created_at'
