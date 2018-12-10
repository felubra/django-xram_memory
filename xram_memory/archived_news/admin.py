from django.contrib import admin

from .models import ArchivedNews, Keyword
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
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

    def _set_manual_insertion(self, instance):
        """
        Se o modelo é novo, mas tem algum campo preenchido, force a flag para inserção manual.
        """
        if instance.pk is None and (instance.authors or instance.images or instance.text or instance.top_image or
                                    instance.summary or instance.keywords or instance.page_pdf_file.name or
                                    instance.title):
            instance.manual_insertion = True

    def save_related(self, request, form, formsets, change):
        super(ArchivedNewsAdmin, self).save_related(
            request, form, formsets, change)
        instance = form.instance
        self._save_keywords_from_the_fetcher(instance)
        self._set_manual_insertion(instance)
