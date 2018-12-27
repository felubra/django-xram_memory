import django_rq
import redis

from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib import messages

from xram_memory.archived_news.models import ArchivedNews, Keyword
from xram_memory.documents.models import ArchivedNewsPDFCapture
from xram_memory.base_models import TraceableAdminModel
from xram_memory.news_fetcher.fetcher import process_news, verify_if_in_archive_org, save_news_as_pdf

from ..forms import ArchivedNewsPDFCaptureStackedInlineForm, ArchivedNewsAdminForm


class ArchivedNewsPDFCaptureInline(admin.TabularInline):
    model = ArchivedNewsPDFCapture
    form = ArchivedNewsPDFCaptureStackedInlineForm


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(TraceableAdminModel):
    MANUAL_INSERTION_TRIGGER_FIELDS = ('authors', 'images', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file',
                                       'title')
    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'archived_news_url')
        }),
        ('Modo de inserção', {
            'classes': ('auto_insert_options',),
            'fields': ('insertion_mode', 'force_basic_processing', 'force_archive_org_processing', 'force_pdf_capture'),
        }),
        ('Informações adicionais', {
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords', 'published_date'),
        }),
    )
    EDIT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords', 'published_date'),
        }),
        ('Avançado', {
            'classes': ('auto_insert_options',),
            'fields': ('force_basic_processing', 'force_archive_org_processing', 'force_pdf_capture'),
        }),
    )
    form = ArchivedNewsAdminForm
    list_display = (
        'id',
        'title',
        'status',
    )
    list_display_links = ('title', 'id',)
    inlines = [
        ArchivedNewsPDFCaptureInline,
    ]

    def get_fieldsets(self, request, obj):
        '''
        Use um conjunto diferente de fieldsets para adição e edição
        '''
        pk = getattr(obj, 'pk', None)
        if pk is None:
            return self.INSERT_FIELDSETS
        else:
            return self.EDIT_FIELDSETS

    def _save_keywords_from_the_fetcher(self, instance, user):
        """
        Crie e inclua palavas-chave extraídas pelo fetcher.
        """
        if hasattr(instance, '_keywords'):
            # TODO: remover palavras sem importância
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
                        # TODO: tratar casos de edição e adição separadamente
                        LogEntry.objects.log_action(
                            user_id=db_keyword.created_by_id,
                            content_type_id=ContentType.objects.get_for_model(
                                db_keyword).pk,
                            object_id=db_keyword.id,
                            object_repr=repr(db_keyword),
                            action_flag=ADDITION,
                            change_message="Palavra-chave inserida indiretamente.")
                # Vincule a palavra-chave a esta notícia arquivada
                if db_keyword:
                    instance.keywords.add(db_keyword)

    def save_model(self, request, obj, form, change):
        # Se estivermos a criar (não editar) um novo registro, determine com base nos campos ou na escolha do usuário se
        # se trata de inserção manual
        if not change:
            if any(field in self.MANUAL_INSERTION_TRIGGER_FIELDS for field in form.changed_data):
                obj.manual_insertion = True
        try:
            django_rq.get_queue().get_job_ids()
        except redis.exceptions.ConnectionError:
            cleaned_data = form.cleaned_data

            force_pdf_capture = cleaned_data.get(
                'force_pdf_capture', False)
            force_archive_org_processing = cleaned_data.get(
                'force_archive_org_processing', False)
            force_basic_processing = cleaned_data.get(
                'force_basic_processing', False)

            if force_basic_processing:
                try:
                    process_news(obj)
                except:
                    messages.add_message(request, messages.WARNING,
                                         "Falha ao buscar informações básicas da notícia.")

            if force_archive_org_processing:
                try:
                    verify_if_in_archive_org(obj)
                except:
                    messages.add_message(request, messages.WARNING,
                                         "Falha ao buscar informações sobre a notícia no Internet Archive.")

            if force_pdf_capture:
                try:
                    save_news_as_pdf(obj)
                except:
                    messages.add_message(request, messages.WARNING,
                                         "Falha ao tentar capturar uma versão em PDF da notícia.")
        finally:
            super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super(ArchivedNewsAdmin, self).save_related(
            request, form, formsets, change)

        instance = form.instance
        self._save_keywords_from_the_fetcher(instance, request.user)
