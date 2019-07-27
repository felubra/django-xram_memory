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
    mime_type = models.fields.CharField(
        verbose_name="Tipo",
        help_text="Tipo do arquivo",
        max_length=255,
        blank=True,
        editable=False)
    is_user_object = models.BooleanField(
        verbose_name="Objeto criado pelo usuário?",
        help_text="Indica se o arquivo foi inserido diretamente por um usuário",
        editable=False,
        default=True)
    document_id = HashidField(
        verbose_name="Código do documento",
        help_text="Código através do qual os visitantes do site podem acessar esse documento.",
        null=True)
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

    published_date = models.DateTimeField(
        verbose_name='Data de publicação',
        help_text='Data da publicação original deste documento',
        blank=True,
        null=True)

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
            with self.file.file.open('rb') as f:
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
        try:
            return self.file.url
        except:
            return ''

    @cachedproperty
    def thumbnail(self):
        """
        Retorna a url para uma miniatura de visualização deste documento.
        """
        try:
            return get_thumbnailer(self.file)['document_thumbnail'].url
        except:
            return ''

    @cachedproperty
    def search_thumbnail(self):
        try:
            return get_thumbnailer(self.file)['thumbnail'].url
        except:
            return ''

    @cachedproperty
    def thumbnails(self):
        """
        Retorna uma lista de thumbnails geradas
        """
        thumbnails_aliases = settings.THUMBNAIL_ALIASES[''].keys()
        generated_thumbnails = {}
        try:
            for alias in thumbnails_aliases:
                generated_thumbnails[alias] = get_thumbnailer(self.file)[
                    alias].url
        except:
            return {}
        else:
            return generated_thumbnails

    @property
    def icons(self):
        try:
            thumbnails = dict(
                (size, self.file.get_thumbnail(
                    {'size': (int(size), int(size)), 'crop': 'scale'}).url)
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
        # limpe o cache das flags/campos, pois o arquivo pode ter mudado
        for attr_name in ['thumbnail', 'search_thumbnail', 'icon', 'thumbnails', 'related_news']:
            try:
                delattr(self, attr_name)
            except AttributeError:
                pass

    def __str__(self):
        if self.document_id is not None:
            return self.document_id.hashid
        else:
            return super().__str__()

    def related_news(self):
        # TODO: limpar o cache dessa propriedade quando a notícia for salva ou quando a(s) captura(s)
        # de notícia for(em) salva(s)
        news_items = []
        try:
            for field_name in ['pdf_capture', 'image_capture']:
                try:
                    for capture in (getattr(self, field_name, None)
                                    .select_related('news')
                                    .only("news__title", "news__slug").all()):
                        news_items.append(capture.news)
                except:
                    continue

        except:
            return []
        else:
            return news_items
