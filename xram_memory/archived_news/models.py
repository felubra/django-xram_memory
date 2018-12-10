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

        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_PUBLISHED_HIDDEN, 'Publicado, mas escondido'),

        (STATUS_ERROR_NO_PROCESS, 'Erro no processamento básico'),
        (STATUS_ERROR_NO_CAPTURE, 'Erro na captura de página')
    )

    url = models.URLField(
        max_length=255, help_text="Endereço da página da notícia", unique=True,
        verbose_name="Endereço")
    title = models.CharField(max_length=255, blank=True,
                             help_text="Título", verbose_name="Título")

    # Define se os campos abaixo serão editados diretamente pelo usuário
    manual_insertion = models.BooleanField(default=False)

    status = models.PositiveIntegerField(
        default=STATUS_NEW, verbose_name="Status", editable=False, choices=STATUS_CHOICES)

    authors = models.TextField(
        blank=True, verbose_name="Autores")

    images = models.TextField(
        blank=True, editable=False, verbose_name="Imagens")

    text = models.TextField(
        blank=True, verbose_name="Texto da notícia")

    top_image = models.ImageField(
        blank=True, verbose_name="Imagem principal")

    summary = models.TextField(
        blank=True, verbose_name="Resumo da notícia")
    keywords = models.TextField(
        blank=True, verbose_name="palavras-chave")

    page_pdf_file = models.FileField(upload_to=saved_pdf_dir,
                                     verbose_name="Arquivo da notícia em PDF",
                                     blank=True)

    class Meta:
        verbose_name = "Archived News"
        verbose_name_plural = "Archived News"

    def __str__(self):
        return self.title

    @property
    def has_error(self):
        return str(self.status)[0] == '5'

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

    def _set_manual_insertion(self):
        # Ignore chamadas a esta função indiretamente invocadas quando dentro de um trabalho de
        # processamento
        if hasattr(self, '_job_processing'):
            return

        # Se o modelo é novo, mas tem os campos preenchidos, force a flag para inserção manual
        if self.pk is None and (self.authors or self.images or self.text or self.top_image or
                                self.summary or self.keywords or self.page_pdf_file.name or
                                self.title):
            self.manual_insertion = True

    def save(self, *args, **kwargs):
        self._set_manual_insertion()
        super().save(*args, **kwargs)
