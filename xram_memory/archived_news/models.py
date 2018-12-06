from django.db import models

# Create your models here.


class ArchivedNews(models.Model):

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

    status = models.PositiveIntegerField(
        default=STATUS_NEW, verbose_name="Status", editable=False, choices=STATUS_CHOICES)

    authors = models.TextField(
        blank=True, verbose_name="Autores", editable=False)

    images = models.TextField(
        blank=True, verbose_name="Imagens", editable=False)
    text = models.TextField(
        blank=True, verbose_name="Texto da notícia", editable=False)
    top_image = models.FilePathField(
        blank=True, verbose_name="Imagem principal", editable=False)

    summary = models.TextField(
        blank=True, verbose_name="Resumo do artigo", editable=False)
    keywords = models.TextField(
        blank=True, verbose_name="palavras-chave", editable=False)

    class Meta:
        verbose_name = "Archived News"
        verbose_name_plural = "Archived News"
