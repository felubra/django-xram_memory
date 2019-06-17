from django.contrib import admin

from xram_memory.base_models import TraceableAdminModel

from .models import Keyword, Subject


class TaxonomyItemAdmin(TraceableAdminModel):
    list_display = (
        'id',
        'name',
    )
    TAXONOMY_ITEM_FIELDSETS = (('Informações básicas', {
        'fields': ('name', )
    }),)
    list_filter = ('created_by', 'modified_by', 'created_at', 'modified_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    list_select_related = (
        'created_by',
        'modified_by',
    )
    ordering = ('name',)

    def get_fieldsets(self, request, obj):
        super().get_fieldsets(request, obj)
        pk = getattr(obj, 'pk', None)
        return self.TAXONOMY_ITEM_FIELDSETS


@admin.register(Keyword)
class KeywordAdmin(TaxonomyItemAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(TaxonomyItemAdmin):
    pass
