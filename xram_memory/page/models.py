from django.db import models
from django.utils.encoding import iri_to_uri
from django.urls import get_script_prefix
from django.utils.text import slugify
from easy_thumbnails.fields import ThumbnailerImageField
from xram_memory.base_models import TraceableEditorialModel
from xram_memory.quill_widget import no_empty_html


# Create your models here.


class StaticPage(TraceableEditorialModel):
    """
    Um modelo para uma página estática.
    """
    title = models.CharField(
        verbose_name="Título",
        help_text="Título",
        max_length=255)
    teaser = models.TextField(
        verbose_name="Resumo ou chamada",
        help_text="Resumo ou chamada",
        null=True,
        blank=True,
        validators=[no_empty_html])
    teaser_text = models.CharField(
        verbose_name="Texto do link de chamada",
        help_text="Texto que será exibido como link para esta página na página inicial",
        null=True,
        max_length=255,
        blank=True)
    url = models.CharField(
        verbose_name="Endereço",
        max_length=100,
        db_index=True)
    body = models.TextField(
        verbose_name="Corpo da página",
        validators=[no_empty_html])
    image = ThumbnailerImageField(
        verbose_name="Imagem",
        null=True,
        blank=True)
    show_in_menu = models.BooleanField(
        verbose_name="Mostrar no menu",
        help_text='Mostrar um link para esta página no menu principal do site',
        default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Force a geração de uma url safa
        self.url = slugify(self.url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
