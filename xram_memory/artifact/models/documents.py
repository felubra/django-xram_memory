import magic
from pathlib import Path
from django.db import models
from filer.models import File
from .artifact import Artifact
from django.conf import settings
from hashid_field import HashidField
from django.utils.text import slugify
from xram_memory.utils import FileValidator
from filer import settings as filer_settings
from boltons.cacheutils import cachedproperty
from django.core.files.base import ContentFile
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.fields import ThumbnailerField
from xram_memory.taxonomy.models import Keyword, Subject


class Document(File):
    """
    Um documento, inserido pelo usuário ou criado pelo sistema
    """
    IMAGE_DOCUMENT_THUMBNAILS_ALIASES = [
        '1280',
        '640',
        '360',
    ]
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
    document_id = HashidField(
        verbose_name="Código do documento",
        help_text="Código através do qual os visitantes do site podem acessar esse documento.",
        null=True
    )
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name="Palavras-chave",
        related_name="%(class)s",
        blank=True,
    )
    subjects = models.ManyToManyField(
        Subject,
        verbose_name="Assuntos",
        related_name="%(class)s",
        blank=True,
    )

    published_date = models.DateTimeField(
        verbose_name='Data de publicação',
        help_text='Data da publicação original deste documento',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    @property
    def published_year(self):
        """
        Retorna o ano de publicação deste documento.
        """
        try:
            # Tente retornar o ano da data de publicação
            return self.published_date.timetuple()[0]
        except AttributeError:
            try:
                # Ou ao menos o ano data de criação dessa Notícia no sistema
                return self.uploaded_at.timetuple()[0]
            except AttributeError:
                return None

    def determine_mime_type(self):
        """
        Utilizando a biblioteca libmagic, determine qual é o mimetype do arquivo deste documento.
        """
        try:
            old_mime_type = self.mime_type
            with self.file.file.open('wb') as f:
                self.mime_type = magic.from_buffer(
                    f.read(1024), mime=True)
            return old_mime_type != self.mime_type
        except:
            self.mime_type = ''
            return False

    def set_document_id(self):
        """
        Gera um document_id se esse Documento não tiver um
        """
        if self.pk is not None and self.document_id is None:
            self.document_id = self.pk
            return True
        return False

    @property
    def document_id_indexing(self):
        try:
            return self.document_id.hashid
        except:
            return ''

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
                return get_thumbnailer(self.file)['document_thumbnail'].url
            except:
                return ''
        return ''

    @cachedproperty
    def search_thumbnail(self):
        if self.file:
            try:
                return get_thumbnailer(self.file)['thumbnail'].url
            except:
                return ''
        return ''

    @cachedproperty
    def thumbnails(self):
        """
        Retorna uma lista de thumbnails geradas
        """
        thumbnails_aliases = ['document_thumbnail']
        generated_thumbnails = {}
        if self.file:
            if getattr(self, 'mime_type', None) and 'image/' in self.mime_type:
                thumbnails_aliases = thumbnails_aliases + \
                    self.IMAGE_DOCUMENT_THUMBNAILS_ALIASES
            try:
                for alias in thumbnails_aliases:
                    generated_thumbnails[alias] = get_thumbnailer(self.file)[
                        alias].url
            except:
                return {}
            else:
                return generated_thumbnails
        return {}

    @property
    def icons(self):
        if self.file.file:
            try:
                thumbnails = dict(
                    (size, self.file.get_thumbnail({
                        'size': (int(size), int(size)),
                        'crop': 'scale'
                    }).url)
                    for size in filer_settings.FILER_ADMIN_ICON_SIZES)
                return thumbnails
            except:
                return 'file'

    @cachedproperty
    def icon(self):
        return self.thumbnail

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # Este será o modelo genérico para todos os tipos de arquivo, em substituição ao do Filer
        return True

    def save(self, *args, **kwargs):
        # Se o documento não tiver nome, use o nome do arquivo
        if not self.name:
            self.name = self.label
        super().save(*args, **kwargs)

    def __str__(self):
        if self.document_id is not None:
            return self.document_id.hashid
        else:
            return super().__str__()
