from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


from xram_memory.archived_news.models import ArchivedNews, Keyword
from xram_memory.documents.models import ArchivedNewsPDFCapture

from ..forms import ArchivedNewsPDFCaptureStackedInlineForm, ArchivedNewsAdminForm


class ArchivedNewsPDFCaptureInline(admin.TabularInline):
    model = ArchivedNewsPDFCapture
    form = ArchivedNewsPDFCaptureStackedInlineForm


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    MANUAL_INSERTION_TRIGGER_FIELDS = ('authors', 'images', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file',
                                       'title')
    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'archived_news_url')
        }),
        ('Modo de inserção', {
            'fields': ('insertion_mode', 'force_basic_processing', 'force_archive_org_processing', 'force_pdf_capture'),
        }),
        ('Informações adicionais', {
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords'),
        }),
    )
    EDIT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords'),
        }),
        ('Avançado', {
            'fields': ('force_basic_processing', 'force_archive_org_processing', 'force_pdf_capture'),
        }),
    )
    form = ArchivedNewsAdminForm
    list_display = (
        'id',
        'title',
        'status',
    )
    inlines = [
        ArchivedNewsPDFCaptureInline,
    ]

    def get_fieldsets(self, request, obj):
        if obj is None:
            return self.INSERT_FIELDSETS
        else:
            return self.EDIT_FIELDSETS

    def _save_keywords_from_the_fetcher(self, instance, user):
        """
        Crie e inclua palavas-chave extraídas pelo fetcher.
        """
        if hasattr(instance, '_keywords'):
            # @todo remover palavras sem importância
            for keyword in instance._keywords:
                try:
                    # tente achar a palavra-chave pelo nome
                    db_keyword = Keyword.objects.get(name=keyword)
                except Keyword.DoesNotExist:
                    # caso não consiga, tente achar pela slug
                    try:
                        db_keyword = Keyword.objects.get(
                            slug=slugify(keyword))
                    # caso não ache, crie uma palavra-chave utilizando o usuário atual
                    except Keyword.DoesNotExist:
                        db_keyword = Keyword.objects.create(
                            name=keyword, slug=slugify(keyword), created_by=user)
                        # @todo: tratar casos de edição e adição separadamente
                        LogEntry.objects.log_action(
                            user_id=db_keyword.created_by_id,
                            content_type_id=ContentType.objects.get_for_model(
                                db_keyword).pk,
                            object_id=db_keyword.id,
                            object_repr=repr(db_keyword),
                            action_flag=ADDITION,
                            change_message="Palavra-chave inserida indiretamente.")
                if db_keyword:
                    instance.keywords.add(db_keyword)

    def save_model(self, request, obj, form, change):
        if change == False and any(field in self.MANUAL_INSERTION_TRIGGER_FIELDS for field in form.changed_data):
            obj.manual_insertion = True

        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super(ArchivedNewsAdmin, self).save_related(
            request, form, formsets, change)
        instance = form.instance
        self._save_keywords_from_the_fetcher(instance, request.user)
