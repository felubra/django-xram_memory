from django.db import models
from django.conf import settings
from django.core.validators import URLValidator

from easy_thumbnails.fields import ThumbnailerField

from xram_memory.utils import FileValidator
from xram_memory.artifact.models import Artifact
from xram_memory.artifact.news_fetcher import NewsFetcher


class Newspaper(Artifact):
    url = models.URLField(
        verbose_name="Endereço",
        help_text="Endereço do site",
        max_length=255,
        unique=True,
        null=False,
        validators=[URLValidator],
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text='A descrição desse veículo/site',
        blank=True,
    )
    logo = ThumbnailerField(
        verbose_name="Logotipo",
        blank=True,
        upload_to='news_sources_logos',
        validators=[FileValidator(
            content_types=settings.VALID_FILE_UPLOAD_IMAGES_MIME_TYPES)],
    )
    published = None
    featured = None
    slug = None
    keywords = None
    subjects = None
    # Remova os campos abaixo herdados de Artifact
    teaser = None
    keywords = None
    subjects = None
    # TODO: campo brand ('marca')

    def set_basic_info(self):
        # TODO: pegar o título correto, não a marca
        newspaper = NewsFetcher.build_newspapaper(self.url)
        self.description, self.title = newspaper.description, newspaper.brand

    @property
    def has_basic_info(self):
        return self.title != self.url

    class Meta:
        verbose_name = "Site de notícias"
        verbose_name_plural = "Sites de notícias"
