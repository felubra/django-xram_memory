from django.db import models

# Create your models here.


class ArchivedNews(models.Model):

    STATUS_NEW = 100
    STATUS_QUEUED = 200
    STATUS_PROCESSED = 300
    STATUS_PUBLISHED = 400
    STATUS_PUBLISHED_HIDDEN = 401
    STATUS_ERROR_NO_PROCESS = 500
    STATUS_ERROR_NO_CAPTURE = 501

    STATUS_CHOICES = (
        (STATUS_NEW, 'Novo'),
        (STATUS_QUEUED, 'Em fila para processamento'),
        (STATUS_PROCESSED, 'Processado'),
        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_PUBLISHED_HIDDEN, 'Escondido'),
        (STATUS_ERROR_NO_PROCESS, 'Erro no processamento'),
        (STATUS_ERROR_NO_CAPTURE, 'Erro na captura')
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
