from django.contrib import admin

from .models import ArchivedNews, Keyword
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify
from django import forms

ARCHIVED_NEWS_MANUAL_INSERTION_TRIGGER_FIELDS = ('authors', 'images', 'text', 'top_image' or
                                                 'summary', 'keywords', 'page_pdf_file',
                                                 'title')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class ArchivedNewsAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ArchivedNewsAdminForm, self).clean()
        title = cleaned_data.get('title', '')
        # Se alguns dos campos acima foram alterandos numa notícia prestes a ser inserida, o título deve ser definido
        if (self.instance.pk is None
                and (self.instance.manual_insertion or
                     any(field in ARCHIVED_NEWS_MANUAL_INSERTION_TRIGGER_FIELDS for field in self.changed_data))
                and not title):
            self.add_error(
                'title', 'Você precisa dar um título para a notícia')


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    form = ArchivedNewsAdminForm
    list_display = (
        'id',
        'title',
        'status',
    )
    fieldsets = (
        ('Informações básicas', {
            'fields': ('url', 'title')
        }),

        ('Informações adicionais', {
            'fields': ('manual_insertion', 'authors', 'text', 'top_image', 'summary', 'keywords', 'page_pdf_file'),
        }),
    )

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
        if change == False and any(field in ARCHIVED_NEWS_MANUAL_INSERTION_TRIGGER_FIELDS for field in form.changed_data):
            obj.manual_insertion = True

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super(ArchivedNewsAdmin, self).save_related(
            request, form, formsets, change)
        instance = form.instance
        self._save_keywords_from_the_fetcher(instance)
