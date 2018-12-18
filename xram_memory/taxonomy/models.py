from django.db import models
from django.template.defaultfilters import slugify

from ..abstract_models import TraceableModel

# Create your models here.


class Keyword(TraceableModel):
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
