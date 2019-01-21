from django.db import models

from ..base_models import TraceableModel
from xram_memory.utils import unique_slugify


class TaxonomyItem(TraceableModel):
    """
    Um simples modelo para salvar uma palavra-chave
    """
    slug = models.SlugField(
        verbose_name="Slug",
        max_length=60,
        unique=True,
        editable=False,
        default=''
    )
    name = models.CharField(
        verbose_name="Nome",
        max_length=60,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # gera uma slug única, considerando as slugs de outros artefatos
        # TODO: somente gerar uma slug nova se não houver slug definida ou conflito de slugs
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Keyword(TaxonomyItem):
    class Meta:
        verbose_name = "Palavra-chave"
        verbose_name_plural = "Palavras-chave"


class Subject(TaxonomyItem):
    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"
