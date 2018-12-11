from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

# Create your models here.
saved_pdf_dir = settings.NEWS_FETCHER_SAVED_DIR_PDF


class Keyword(models.Model):
    """
    Um simples modelo para salvar uma palavra-chave
    """
    slug = models.SlugField(max_length=60, unique=True,
                            editable=False, default='')
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Palavra-chave"
        verbose_name_plural = "Palavras-chave"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArchivedNews(models.Model):
    """
    Guarda uma notíca arquivada, enviada tanto manualmente ou obtida automaticamente pelo sistema do
    site.
    """

    STATUS_NEW = 100
    # Em fila
    STATUS_QUEUED_BASIC_INFO = 200
    STATUS_QUEUED_PAGE_CAPTURE = 201
    # Processado
    STATUS_PROCESSED_BASIC_INFO = 300
    STATUS_PROCESSED_PAGE_CAPTURE = 301
    STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED = 302
    # Publicado
    STATUS_PUBLISHED = 400
    STATUS_PUBLISHED_HIDDEN = 401
    # Erros
    STATUS_ERROR_NO_PROCESS = 500
    STATUS_ERROR_NO_CAPTURE = 501

    STATUS_CHOICES = (
        (STATUS_NEW, 'Novo'),

        (STATUS_QUEUED_BASIC_INFO, 'Em fila para buscar informações básicas'),
        (STATUS_QUEUED_PAGE_CAPTURE, 'Em fila para capturar a página'),


        (STATUS_PROCESSED_BASIC_INFO, 'Processado com informações básicas'),
        (STATUS_PROCESSED_PAGE_CAPTURE, 'Processado com captura de página'),
        (STATUS_PROCESSED_ARCHIVED_NEWS_FETCHED,
         'Processado com informações da página arquivada no Internet Archive'),

        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_PUBLISHED_HIDDEN, 'Publicado, mas escondido'),

        (STATUS_ERROR_NO_PROCESS, 'Erro no processamento básico'),
        (STATUS_ERROR_NO_CAPTURE, 'Erro na captura de página')
    )

    url = models.URLField(
        max_length=255, help_text="Endereço original da notícia",
        verbose_name="Endereço", unique=True, null=True, blank=True)

    archived_news_url = models.URLField(
        max_length=255, help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>",
        verbose_name="Endereço no Internet Archive", unique=True, null=True, blank=True)

    title = models.CharField(max_length=255, blank=True,
                             help_text="Título da notícia", verbose_name="Título")

    status = models.PositiveIntegerField(
        default=STATUS_NEW, verbose_name="Status", editable=False, choices=STATUS_CHOICES)

    authors = models.TextField(
        blank=True, verbose_name="Autores", help_text='Nomes dos autores, separados por vírgula')

    images = models.TextField(
        blank=True, editable=False, verbose_name="Imagens", help_text="Imagens associadas a esta notícia")

    text = models.TextField(
        blank=True, verbose_name="Texto da notícia", help_text="Texto integral da notícia")

    top_image = models.ImageField(
        blank=True, verbose_name="Imagem principal")

    summary = models.TextField(
        blank=True, verbose_name="Resumo da notícia")

    keywords = models.ManyToManyField(
        Keyword, blank=True, verbose_name="Palavras-chave")

    page_pdf_file = models.FileField(upload_to=saved_pdf_dir,
                                     verbose_name="Captura da notícia em PDF",
                                     blank=True)

    # Flags
    force_basic_processing = models.BooleanField(
        "Buscar automaticamente informações sobre a notícia", default=True,
        help_text="Marque se deseja incluir essa notícia para processamento automático.")
    force_archive_org_processing = models.BooleanField(
        "Buscar informações no Archive.org", default=True,
        help_text="Marque se deseja buscar uma versão arquivada desta notícia no <a href='https://archive.org/'>Archive.org</a>.")
    force_pdf_capture = models.BooleanField(
        "Capturar a notícia em formato PDF", default=True,
        help_text="Marque se deseja capturar essa notícia em formato PDF.")

    class Meta:
        verbose_name = "Archived News"
        verbose_name_plural = "Archived News"

    def __str__(self):
        return self.title

    @property
    def has_error(self):
        return str(self.status)[0] == '5'

    @property
    def needs_reprocessing(self):
        return self.force_basic_processing or self.force_archive_org_processing or self.force_pdf_capture

    @property
    def has_basic_info(self):
        return (bool(self.text) or bool(self.summary) or bool(self.authors) or bool(self.keywords) or
                bool(self.top_image) or bool(self.images))

    @property
    def has_pdf_capture(self):
        return bool(self.page_pdf_file)

    @property
    def has_web_archive(self):
        return bool(self.archived_news_url)

    @property
    def is_published(self):
        return str(self.status)[0] == '4'

    @property
    def is_processed(self):
        return str(self.status)[0] == '3'

    @property
    def is_queued(self):
        return str(self.status)[0] == '2'

    @property
    def is_new(self):
        return self.status == ArchivedNews.STATUS_NEW
