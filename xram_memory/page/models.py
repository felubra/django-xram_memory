from django.db import models
from django.utils.encoding import iri_to_uri
from django.urls import get_script_prefix
from django.utils.text import slugify
from easy_thumbnails.fields import ThumbnailerImageField


# Create your models here.
from xram_memory.base_models import TraceableEditorialModel


class StaticPage(TraceableEditorialModel):
    title = models.CharField(
        verbose_name="Título",
        help_text="Título",
        max_length=255,
    )
    teaser = models.TextField(
        verbose_name="Resumo ou chamada",
        help_text="Resumo ou chamada",
        null=True,
        blank=True,
    )
    url = models.CharField(
        verbose_name="Endereço",
        max_length=100,
        db_index=True
    )
    body = models.TextField(
        verbose_name="Corpo da página"
    )
    image = ThumbnailerImageField(
        verbose_name="Imagem",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Force a geração de uma url safa
        self.url = slugify(self.url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
