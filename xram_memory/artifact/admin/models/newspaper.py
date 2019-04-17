from django.contrib import admin

from xram_memory.artifact.models import Newspaper


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'url',
        'logo',
    )
    list_filter = ('created_at', 'modified_at', )
    date_hierarchy = 'created_at'
    list_select_related = (
        'created_by',
        'modified_by',
    )
