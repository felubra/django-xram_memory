from django.contrib import admin

from .models import ArchivedNews


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'keywords',
    )
    fieldsets = (
        ('Informações básicas', {
            'fields': ('url', 'title')
        }),

        ('Informações adicionais', {
            'fields': ('manual_insertion', 'authors', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file'),
        }),
    )
