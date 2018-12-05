from django.db import models

# Create your models here.


class ArchivedNews(models.Model):
    url = models.URLField(
        max_length=255, help_text="Endereço da página da notícia", unique=True,
        verbose_name="Endereço")
    title = models.CharField(max_length=255, blank=True,
                             help_text="Título", verbose_name="Título")

    downloaded = models.BooleanField(
        default=False, verbose_name="Baixado?", editable=False)

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
