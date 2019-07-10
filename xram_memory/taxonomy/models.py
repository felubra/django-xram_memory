from django.db import models
from ..base_models import TraceableModel
from xram_memory.utils import no_empty_html
from xram_memory.utils import unique_slugify
from boltons.cacheutils import cachedproperty
from django.core.exceptions import ValidationError


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
        unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Keyword(TaxonomyItem):
    class Meta:
        verbose_name = "Palavra-chave"
        verbose_name_plural = "Palavras-chave"


class Subject(TaxonomyItem):
    description = models.TextField(
        verbose_name="Descrição",
        help_text='Uma descrição detalhada para este Assunto',
        blank=True)

    @cachedproperty
    def cover(self):
        """
        Retorna uma imagem de captura de uma notícia aleatória, relacionada a este assunto.
        """
        try:
            return self.news.filter(image_capture__isnull=False).order_by('?')[0:1][0].thumbnails['image_capture']
        except:
            return ''

    @cachedproperty
    def has_description(self):
        """
        Indica se o assunto tem descrição, lida com tags HTML em branco.
        """
        try:
            if self.description:
                no_empty_html(self.description)
                return True
            else:
                return False
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.has_description:
            self.description = ''
        super().save(*args, **kwargs)
        for attr_name in ['cover', 'has_description']:
            try:
                delattr(self, attr_name)
            except AttributeError:
                pass

    class Meta:
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"
