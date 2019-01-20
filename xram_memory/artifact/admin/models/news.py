import django_rq
import redis

from django.contrib import admin
from django.template.defaultfilters import slugify

from xram_memory.base_models import TraceableAdminModel
from xram_memory.artifact.models import News, NewsPDFCapture
from xram_memory.taxonomy.models import Subject, Keyword

from ..forms.news import NewsPDFCaptureStackedInlineForm, NewsAdminForm


class NewsPDFCaptureInline(admin.TabularInline):
    model = NewsPDFCapture
    form = NewsPDFCaptureStackedInlineForm


@admin.register(News)
class NewsAdmin(TraceableAdminModel):
    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'title',   'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('teaser', 'body',  'published_date', 'authors', 'slug'),
        }),
        ('Classificação do conteúdo', {
            'fields': ('subjects', 'keywords', ),
        }),
        ('Avançado', {
            'fields': ('set_basic_info', 'fetch_archived_url', 'add_pdf_capture')
        })
    )
    EDIT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'title',  'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('teaser', 'body',  'published_date', 'authors', 'slug'),
        }),
        ('Classificação do conteúdo', {
            'fields': ('subjects', 'keywords', ),
        }),
        ('Avançado', {
            'fields': ('set_basic_info', 'fetch_archived_url', 'add_pdf_capture')
        })
    )
    form = NewsAdminForm
    list_display = (
        'id',
        'title',
    )
    list_display_links = ('title', 'id',)
    inlines = [
        NewsPDFCaptureInline,
    ]
    search_fields = ('title',)
    date_hierarchy = 'modified_at'
    prepopulated_fields = {"slug": ("title",)}

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.slug:
            self.prepopulated_fields = {}
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

    def get_fieldsets(self, request, obj):
        '''
        Use um conjunto diferente de fieldsets para adição e edição
        '''
        # TODO: colocar o fieldset das capturas de página antes do fieldset com as informações gerais
        super(NewsAdmin, self).get_fieldsets(request, obj)
        pk = getattr(obj, 'pk', None)
        if pk is None:
            return self.INSERT_FIELDSETS
        else:
            return self.EDIT_FIELDSETS + self.fieldsets

    def save_related(self, request, form, formsets, change):
        super(NewsAdmin, self).save_related(request, form, formsets, change)
        instance = form.instance
        # precisamos adicionar as palavras-chave novamente aqui, pois as associações feitas na chamada no método save
        # serão desfeitas pelo django admin - https://timonweb.com/posts/many-to-many-field-save-method-and-the-django-admin/
        instance.add_fetched_keywords()
