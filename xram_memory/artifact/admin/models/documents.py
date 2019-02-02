from django.contrib import admin
from xram_memory.artifact.models import Document
from xram_memory.base_models import TraceableEditorialAdminModel
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerField


@admin.register(Document)
class DocumentAdmin(TraceableEditorialAdminModel):
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
    FIELDSETS = (
        ('Arquivo', {
            'fields': ('file',)
        }),
        ('Informações adicionais', {
            'fields': ('title', 'teaser', 'slug',)
        }),
        ('Classificação do conteúdo', {
            'fields': ('subjects', 'keywords', ),
        }),
    )

    formfield_overrides = {
        ThumbnailerField: {'widget': ImageClearableFileInput},
    }

    def get_fieldsets(self, request, obj):
        return self.FIELDSETS + self.COMMON_FIELDSETS
