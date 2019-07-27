from django import forms
from django.contrib import admin
from .models import Keyword, Subject
from xram_memory.base_models import TraceableAdminModel
from xram_memory.quill_widget import QuillWidget, make_editor_opt, TEASER_EDITOR_OPTIONS


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
        return self.TAXONOMY_ITEM_FIELDSETS


@admin.register(Keyword)
class KeywordAdmin(TaxonomyItemAdmin):
    pass


class SubjectAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': QuillWidget(attrs=make_editor_opt('')),
        }


@admin.register(Subject)
class SubjectAdmin(TaxonomyItemAdmin):
    form = SubjectAdminForm

    def get_fieldsets(self, request, obj):
        super().get_fieldsets(request, obj)
        return self.TAXONOMY_ITEM_FIELDSETS + (('Informações adicionais', {
            'fields': ('description', )
        }), ('Opções de publicação', {
            'fields': ('featured', )
        }),)
