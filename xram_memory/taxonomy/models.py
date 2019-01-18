from django.db import models
from django.template.defaultfilters import slugify

from ..base_models import TraceableModel

# Create your models here.


class TaxonomyItem(TraceableModel):
    """
    Um simples modelo para salvar uma palavra-chave
    """
    slug = models.SlugField(max_length=60, unique=True,
                            editable=False, default='')
    name = models.CharField(max_length=60, verbose_name="Nome")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Keyword(TaxonomyItem):
    class Meta:
        verbose_name = "Palavra-chave"
        verbose_name_plural = "Palavras-chave"


class Subject(TaxonomyItem):
    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"
