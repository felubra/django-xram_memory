from django.db import models
from xram_memory.utils import unique_slugify
from xram_memory.base_models import TraceableEditorialModel
from xram_memory.taxonomy.models import Keyword, Subject


class Artifact(TraceableEditorialModel):
    """
    Classe abstrata para todos os objetos-artefato do acervo
    """
    # TODO: lidar com a exigência do título
    title = models.CharField(
        verbose_name="Título",
        help_text="Título",
        max_length=255,
        blank=True,
    )
    teaser = models.TextField(
        verbose_name="Resumo ou chamada",
        help_text="Resumo ou chamada",
        blank=True,
    )
    # TODO: adicionar um help_text para `slug`
    slug = models.SlugField(
        verbose_name="Slug",
        help_text="",
        blank=True,
    )
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name="Palavras-chave",
        blank=True,
    )
    subjects = models.ManyToManyField(
        Subject,
        verbose_name="Assuntos",
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # gera uma slug única, considerando as slugs de outros artefatos
        # TODO: somente gerar uma slug nova se não houver slug definida ou conflito de slugs
        unique_slugify(self, self.title)
        if not self.title:
            raise ValueError(
                "Não é possível criar um artefato sem título.")
        super(Artifact, self).save(*args, **kwargs)
