from django.contrib import admin

from .models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    list_filter = ('created_by', 'modified_by', 'created_at', 'modified_at')
    raw_id_fields = ('items',)
    date_hierarchy = 'created_at'
