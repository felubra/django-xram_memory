import magic
from pathlib import Path
from django.db import models
from filer.models import File
from .artifact import Artifact
from django.conf import settings
from django.utils.text import slugify
from xram_memory.utils import FileValidator
from boltons.cacheutils import cachedproperty
from django.core.files.base import ContentFile
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerField


class Document(File):
    """
    Um documento, inserido pelo usuário ou criado pelo sistema
    """
    mime_type = models.fields.CharField(
        verbose_name="Tipo",
        help_text="Tipo do arquivo",
        max_length=255,
        blank=True,
        editable=False,
    )
    is_user_object = models.BooleanField(
        verbose_name="Objeto criado pelo usuário?",
        help_text="Indica se o arquivo foi inserido diretamente por um usuário",
        editable=False,
        default=True,
    )

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def determine_mime_type(self):
        """
        Utilizando a biblioteca libmagic, determine qual é o mimetype do arquivo deste documento.
        """
        try:
            self.mime_type = magic.from_buffer(
                self.file.file.read(1024), mime=True)
            self.file.file.seek(0)
        except:
            self.mime_type = ''

    @property
    def file_indexing(self):
        """
        Propriedade usada para indexar a URL para este documento.
        """
        if self.file:
            return self.file.url

    @cachedproperty
    def thumbnail(self):
        """
        Retorna a url para uma miniatura de visualização deste documento.
        """
        if self.file:
            try:
                return get_thumbnailer(self.file)['thumbnail'].url
            except:
                return None

    @cachedproperty
    def icon(self):
        return self.thumbnail

    def file_data_changed(self, post_init=False):
        '''
        Verifique com a classe pai se o arquivo foi modificado e, caso afirmativo, recalcule seu mime_type.
        '''
        changed = super().file_data_changed(post_init)
        if changed:
            self.determine_mime_type()
        return changed
