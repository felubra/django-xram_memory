from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from ..forms.news import NewsPDFCaptureStackedInlineForm, NewsAdminForm, NewsImageCaptureStackedInlineForm
from xram_memory.artifact.models import News, NewsPDFCapture, NewsImageCapture
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.sites import site as default_site, AdminSite
from xram_memory.base_models import TraceableEditorialAdminModel
from xram_memory.taxonomy.models import Subject, Keyword
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from xram_memory.artifact.tasks import add_news_task
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from xram_memory.utils import celery_is_avaliable
from tags_input import admin as tags_input_admin
from django.core.validators import URLValidator
from django.contrib.staticfiles import finders
from django.db.utils import IntegrityError
from django.utils.html import format_html
from django.shortcuts import render
from django.contrib import messages
from django.contrib import admin
from django.urls import reverse
from django.urls import path
from loguru import logger
from django import forms
from django import forms


class NewsPDFCaptureInline(admin.TabularInline):
    model = NewsPDFCapture
    form = NewsPDFCaptureStackedInlineForm


class NewsImageCaptureInline(admin.TabularInline):
    model = NewsImageCapture
    form = NewsImageCaptureStackedInlineForm


class URLForm(forms.Form):
    fieldsets = ()
    urls = forms.fields.CharField(widget=forms.widgets.Textarea, label="Endereços",
                                  help_text="Insira os endereços das notícias, um por linha")

    def clean_urls(self, *args, **kwargs):
        """
        Valida cada uma das urls informadas.
        """
        urls = self.cleaned_data['urls']
        if not urls:
            raise ValidationError("É necessário informar uma URL.")
        # 1) separe por linha, construa uma array com os valores
        urls = urls.split()

        url_validator = URLValidator()

        def is_valid(value):
            try:
                url_validator(value)
                return True
            except ValidationError:
                return False

        # 3) Filtre a array para somente urls válidas
        urls = [url for url in urls if is_valid(url)]
        # 4) Se não houver urls válidas, crie um erro de validação
        if not len(urls):
            raise ValidationError('Todos endereços informados são inválidos.',
                                  code='invalid',
                                  params={'urls': urls},
                                  )
        return urls


@admin.register(News)
class NewsAdmin(TraceableEditorialAdminModel, tags_input_admin.TagsInputAdmin):
    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'title',   'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('teaser', 'body',  'published_date', 'authors', 'slug', ),
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
            'fields': ('teaser', 'body',  'published_date', 'authors', 'slug', ),
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
        'created_at',
        'modified_at',
        'captures',
    )
    list_display_links = ('title', 'id',)
    inlines = [
        NewsPDFCaptureInline,
        NewsImageCaptureInline,
    ]
    search_fields = ('title',)
    date_hierarchy = 'modified_at'
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = (
        'image_capture',
    )

    def captures(self, obj):
        def missing_label(status):
            return '' if status[0] else 'missing'

        def get_title(status):
            return status[1] if status[0] else status[2]

        icons_and_captures = {
            'info': (obj.has_basic_info, 'Tem informações básicas', 'Sem informações básicas',),
            'picture_as_pdf': (obj.has_pdf_capture, 'Tem captura em pdf', 'Sem captura em pdf',),
            'filter': (obj.has_image, 'Tem imagem', 'Sem imagem',),
        }

        icon_elements = [
            '<i class="material-icons capture_status_icon {capture_status}" title="{title}">{icon_name}</i>'.format(
                icon_name=icon_name,
                capture_status=missing_label(info),
                title=get_title(info)
            )
            for icon_name, info in icons_and_captures.items()
        ]
        html = format_html(
            '<div class="captures_info">{icon_elements}</div>'.format(icon_elements=''.join(icon_elements)))
        return html
    captures.short_description = 'Capturas'

    def get_tag_fields(self):
        return ['subjects', 'keywords']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.slug:
            self.prepopulated_fields = {}
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

    def get_fieldsets(self, request, obj):
        """
        Use um conjunto diferente de fieldsets para adição e edição
        """
        # TODO: colocar o fieldset das capturas de página antes do fieldset com as informações gerais
        super().get_fieldsets(request, obj)
        pk = getattr(obj, 'pk', None)
        if pk is None:
            return self.INSERT_FIELDSETS
        else:
            return self.EDIT_FIELDSETS + self.COMMON_FIELDSETS

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        # precisamos adicionar as palavras-chave novamente aqui, pois as associações feitas na chamada no método save
        # serão desfeitas pelo django admin - https://timonweb.com/posts/many-to-many-field-save-method-and-the-django-admin/
        instance.add_fetched_keywords()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('insert_bulk/', self.admin_site.admin_view(self.bulk_insertion),
                 name='news_bulk_insertion'),
        ]
        return my_urls + urls

    @never_cache
    def bulk_insertion(self, request):
        """
        Controller para a página de inserção em massa de notícias.
        """
        if celery_is_avaliable():
            if request.method == 'POST':
                # crie uma instância do formulário URLForm para validar os dados.
                form = URLForm(request.POST)
                if form.is_valid():
                    # pegue as urls sanitizadas
                    urls, = form.cleaned_data.values()
                    # agende a execução de 5 tarefas por vez para criar notícias com base urls
                    urls_and_user_id = ((url, request.user.id) for url in urls)
                    add_news_task.throws = (IntegrityError,)
                    add_news_task.chunks(
                        urls_and_user_id, 5).group().apply_async()
                    logger.info(
                        'O usuário {username} solicitou a inserção de {n} notícia(s) de uma só vez pela interface administrativa.'.format(
                            username=request.user.username, n=len(urls)
                        )
                    )
                    # dê um aviso das urls inseridas
                    messages.add_message(request, messages.INFO,
                                         '{} endereço(s) de notícia adicionado(s) à fila para criação.'.format(len(urls)))
                    # redirecione para a página inicial
                    return HttpResponseRedirect(reverse("admin:artifact_news_changelist"))
                else:
                    # renderize novamente o formulário para dar oportunidade do usuário corrigir os erros
                    context = dict(
                        # Include common variables for rendering the admin template.
                        self.admin_site.each_context(request),
                        form=form,
                        title='Inserir notícias',
                    )
                    return TemplateResponse(request, "news_bulk_insertion.html", context)
            else:
                # crie um formulário vazio
                form = URLForm()
                context = dict(
                    # Include common variables for rendering the admin template.
                    self.admin_site.each_context(request),
                    form=form,
                    title='Inserir notícias',
                )
                return TemplateResponse(request, "news_bulk_insertion.html", context)
        else:
            messages.add_message(request, messages.ERROR,
                                 'Não é possível usar esta funcionalidade no momento, porque o servidor de filas não está disponível. Se o erro persistir, contate o administrador.')
            return HttpResponseRedirect(reverse("admin:artifact_news_changelist"))
