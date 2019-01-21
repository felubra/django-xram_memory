from django.db import models
from xram_memory.utils import unique_slugify
from xram_memory.base_models import TraceableEditorialModel
from xram_memory.taxonomy.models import Keyword, Subject


class Artifact(TraceableEditorialModel):
    # TODO: lidar com a exigência do título
    title = models.CharField(max_length=255, blank=True,
                             help_text="Título", verbose_name="Título")
    teaser = models.TextField(
        help_text="Resumo ou chamada", verbose_name="Resumo ou chamada", blank=True)

    # TODO: adicionar um help_text para `slug`
    slug = models.SlugField(help_text="", verbose_name="Slug", blank=True)

    keywords = models.ManyToManyField(
        Keyword, blank=True, verbose_name="Palavras-chave")
    subjects = models.ManyToManyField(
        Subject, blank=True, verbose_name="Assuntos")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        if not self.title:
            raise ValueError(
                "Não é possível criar um artefato sem título.")
        super(Artifact, self).save(*args, **kwargs)
