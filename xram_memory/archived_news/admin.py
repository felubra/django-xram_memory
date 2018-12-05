from django.contrib import admin

from .models import ArchivedNews


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'title',
        'status',
        'authors',
        'images',
        'text',
        'top_image',
        'summary',
        'keywords',
    )
