from django.contrib import admin
from xram_memory.artifact.models import Document
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
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Arquivo', {
            'fields': ('file',)
        }),
        ('Informações adicionais', {
            'fields': ('title', 'teaser', 'slug',)
        }),
        ('Classificação do conteúdo', {
            'fields': ('subjects', 'keywords', ),
        }),
        ('Informações editoriais', {
            'fields': (('published', 'featured'),
                       'created_by',
                       'modified_by',
                       'created_at',
                       'modified_at',)
        }),
    )
