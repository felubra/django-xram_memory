from django.contrib import admin

from .models import ArchivedNews, Keyword
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify
from django import forms
from django.forms import ValidationError


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class ArchivedNewsAdminForm(forms.ModelForm):
    INSERTION_AUTOMATIC = 0
    INSERTION_MANUAL = 1

    INSERTION_MODES = (
        (INSERTION_AUTOMATIC, "Inserção automática"),
        (INSERTION_MANUAL, "Inserção manual"),
    )

    insertion_mode = forms.ChoiceField(required=False,
                                       widget=forms.RadioSelect, choices=INSERTION_MODES, label="Modo de inserção")

    def __init__(self, *args, **kwargs):
        super(ArchivedNewsAdminForm, self).__init__(*args, **kwargs)
        self.initial['insertion_mode'] = self.INSERTION_AUTOMATIC
        if not self.instance.pk is None:
            self.fields['force_basic_processing'].label = "Reinserir na fila para processamento automático"
            self.fields['force_basic_processing'].help_text = "Marque se deseja reinserir essa notícia para processamento automático.<br/><strong>NOTA:</strong> isso sobrescreverá qualquer informação anterior."

            self.fields['force_archive_org_processing'].label = "Reinserir na fila para buscar informações no Archive.org"
            self.fields['force_archive_org_processing'].help_text += "<br/><strong>NOTA:</strong> isso sobrescreverá qualquer informação anterior."

            self.fields['force_pdf_capture'].label = "Gerar uma nova captura de página"
            self.fields['force_pdf_capture'].help_text += "<br/><strong>NOTA:</strong> isso substituirá a captura de página anterior."

    def clean(self):
        cleaned_data = super(ArchivedNewsAdminForm, self).clean()

        title = cleaned_data.get('title', '')
        url = cleaned_data.get('url', '')
        archived_news_url = cleaned_data.get('archived_news_url', '')
        insertion_mode = cleaned_data.get(
            'insertion_mode', self.INSERTION_AUTOMATIC)

        force_pdf_capture = cleaned_data.get('force_pdf_capture', False)
        force_archive_org_processing = cleaned_data.get(
            'force_archive_org_processing', False)
        force_basic_processing = cleaned_data.get(
            'force_basic_processing', False)

        manual_insert = insertion_mode == self.INSERTION_MANUAL or not (
            force_pdf_capture or force_archive_org_processing or force_basic_processing)

        # Se alguns dos campos acima foram alterados numa notícia prestes a ser inserida, o título deve ser definido
        if self.instance.pk is None:
            if manual_insert and not title:
                self.add_error(
                    'title', 'Você precisa dar um título para a notícia')

        # A notícia deve conter ao menos uma url, seja a original ou seja a arquivada
        if not (url or archived_news_url):
            self.add_error(
                'url', 'Preencha este campo')
            self.add_error(
                'archived_news_url', 'Preencha este campo')
            raise ValidationError(
                "Você precisa definir ao menos um endereço para a notícia")


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
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file'),
        }),
    )
    EDIT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('url', 'archived_news_url')
        }),

        ('Informações adicionais', {
            'fields': ('title', 'authors', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file'),
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

    def get_fieldsets(self, request, obj):
        if obj is None:
            return self.INSERT_FIELDSETS
        else:
            return self.EDIT_FIELDSETS

    def _save_keywords_from_the_fetcher(self, instance):
        """
        Crie e inclua palavas-chave extraídas pelo fetcher.
        """
        if hasattr(instance, '_keywords'):
            # @todo remover palavras sem importância
            for keyword in instance._keywords:
                try:
                    db_keyword, _ = Keyword.objects.get_or_create(name=keyword)
                except IntegrityError:
                    db_keyword, _ = Keyword.objects.get(slug=slugify(keyword))
                if db_keyword:
                    instance.keywords.add(db_keyword)

    def save_model(self, request, obj, form, change):
        if change == False and any(field in self.MANUAL_INSERTION_TRIGGER_FIELDS for field in form.changed_data):
            obj.manual_insertion = True
        # @todo migrar para um sinal?
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super(ArchivedNewsAdmin, self).save_related(
            request, form, formsets, change)
        instance = form.instance
        self._save_keywords_from_the_fetcher(instance)
