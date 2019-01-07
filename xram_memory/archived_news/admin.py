from django.contrib import admin

from .models import ArchivedNews


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    list_filter = ('created_by', 'modified_by', 'created_at', 'modified_at')
    date_hierarchy = 'created_at'
