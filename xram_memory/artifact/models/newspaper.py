from xram_memory.artifact.news_fetcher import NewsFetcher
from xram_memory.logger.decorators import log_process
from easy_thumbnails.fields import ThumbnailerField
from xram_memory.base_models import TraceableModel
from django.core.files import File as DjangoFile
from django.core.validators import URLValidator
from xram_memory.utils import FileValidator
from django.db import transaction
from django.conf import settings
from django.db import models
from pathlib import Path
import requests
import tempfile
import favicon
import os


class Newspaper(TraceableModel):
    title = models.CharField(
        verbose_name="Título",
        help_text="Título",
        max_length=255,
        blank=True,
    )
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

    def __str__(self):
        return self.title
    # TODO: campo brand ('marca')

    @log_process(operation="adicionar informações básicas para um jornal")
    def set_basic_info(self):
        # TODO: pegar o título correto, não a marca
        newspaper = NewsFetcher.build_newspaper(self.url)
        self.description, self.title = newspaper.description, newspaper.brand

    @log_process(operation="adicionar um logo para um jornal")
    def set_logo_from_favicon(self):
        icons = [icon for icon in favicon.get(
            self.url) if icon.format in ['png', 'jpeg', 'jpg', 'gif']]
        if len(icons):
            icon = icons[0]
            file_ext = Path(icon.url).suffix
            response = requests.get(icon.url, stream=True)
            fd, file_path, = tempfile.mkstemp()
            filename = self.title + '_logo' + file_ext
            with open(fd, 'wb+') as image:
                for chunk in response.iter_content(1024):
                    image.write(chunk)
                with transaction.atomic():
                    django_file = DjangoFile(image, name=filename)
                    # apague o logotipo já existente, se for o caso
                    if self.has_logo:
                        self.logo.delete()
                    self.logo.save(filename, django_file)
            os.remove(file_path)
        else:
            raise ValueError(
                "Nenhum ícone válido foi encontrado para o jornal/site")

    @property
    def has_basic_info(self):
        return self.title != self.url

    @property
    def has_logo(self):
        if self.pk is None:
            return False
        else:
            try:
                logo_file = self.logo.file
                return True
            except:
                return False

    class Meta:
        verbose_name = "Site de notícias"
        verbose_name_plural = "Sites de notícias"
