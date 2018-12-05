from django.db import models

# Create your models here.


class ArchivedNews(models.Model):

    STATUS_NEW = 1
    STATUS_QUEUED = 2
    STATUS_PROCESSED = 3
    STATUS_PUBLISHED = 4
    STATUS_HIDDEN = 5

    STATUS_CHOICES = (
        (STATUS_NEW, 'Novo'),
        (STATUS_QUEUED, 'Em fila para processamento'),
        (STATUS_PROCESSED, 'Processado'),
        (STATUS_PUBLISHED, 'Publicado'),
        (STATUS_HIDDEN, 'Escondido'),
    )

    url = models.URLField(
        max_length=255, help_text="Endereço da página da notícia", unique=True,
        verbose_name="Endereço")
    title = models.CharField(max_length=255, blank=True,
                             help_text="Título", verbose_name="Título")

    status = models.PositiveIntegerField(
        default=STATUS_NEW, verbose_name="Baixado?", editable=False, choices=STATUS_CHOICES)

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
