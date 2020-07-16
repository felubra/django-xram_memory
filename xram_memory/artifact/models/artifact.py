from django.db import models
from xram_memory.utils import unique_slugify
from xram_memory.base_models import TraceableEditorialModel
from xram_memory.taxonomy.models import Keyword, Subject


class Artifact(TraceableEditorialModel):
    """
    Classe abstrata para todos os objetos-artefato do acervo
    """
    title = models.CharField(
        verbose_name="Título",
        help_text="Título",
        max_length=255,
        blank=True)
    teaser = models.TextField(
        verbose_name="Resumo ou chamada",
        help_text="Resumo ou chamada",
        null=True,
        blank=True)
    slug = models.SlugField(
        verbose_name="Endereço",
        help_text="Parte do endereço pelo qual este artefato poderá ser acessado",
        blank=True)
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name="Palavras-chave",
        related_name="%(class)s",
        blank=True)
    subjects = models.ManyToManyField(
        Subject,
        verbose_name="Assuntos",
        related_name="%(class)s",
        blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.title not in (None, ''):
            return self.title
        else:
            return '(sem título)'

    def save(self, *args, **kwargs):
        # gera uma slug única, considerando as slugs de outros artefatos

        unique_slugify(self, self.title)
        if not self.title:
            raise ValueError(
                "Não é possível criar um artefato sem título.")
        # limite o título ao tamanho máximo do campo
        self.title = self.title[:255]
        super().save(*args, **kwargs)

    @property
    def keywords_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [keyword.name for keyword in self.keywords.all()]

    @property
    def subjects_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [subject.name for subject in self.subjects.all()]

    @property
    def null_field_indexing(self):
        """null_field for indexing.

        Used in Elasticsearch indexing/tests of `isnull` functional filter.
        """
        return None
