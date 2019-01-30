from django.contrib import admin
from xram_memory.base_models import TraceableEditorialAdminModel
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField

from .models import StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(TraceableEditorialAdminModel):
    list_display = (
        'id',
        'title',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'published',
        'featured',
    )
    prepopulated_fields = {'url': ('title', ), }

    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('title', 'teaser', 'body',)
        }),

        ('Informações adicionais', {
            'fields': ('url', 'image'),
        }),
    )
    list_display_links = ('title', 'id',)
    date_hierarchy = 'created_at'
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput},
    }

    def get_fieldsets(self, request, obj):
        """
        Use um conjunto diferente de fieldsets para adição e edição
        """
        # TODO: colocar o fieldset das capturas de página antes do fieldset com as informações gerais
        super().get_fieldsets(request, obj)
        return self.INSERT_FIELDSETS + self.COMMON_FIELDSETS
