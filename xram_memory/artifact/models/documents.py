import magic
from pathlib import Path

from django.conf import settings
from django.db import models
from .artifact import Artifact
from django_rq import job


class Document(Artifact):
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
    file_size = models.fields.CharField(
        verbose_name="Tamanho",
        help_text="Tamanho do arquivo em bytes",
        default='0',
        editable=False,
        max_length=100,
    )
    is_user_object = models.BooleanField(
        verbose_name="Objeto criado pelo usuário?",
        help_text="Indica se o arquivo foi inserido diretamente por um usuário",
        editable=False,
        default=True,
    )
    file = NotImplemented

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.file.name
        super(Document, self).save(*args, **kwargs)

    def determine_mime_type(self):
        """
        Utilizando a biblioteca libmagic, determine qual é o mimetype do arquivo deste documento.
        """
        try:
            self.mime_type = magic.from_file(self.file.path, mime=True)
        except:
            self.mime_type = ''

    def determine_file_size(self):
        try:
            self.file_size = self.file.size
        except:
            self.file_size = '0'


class PDFDocument(Document):
    """
    Um documento PDF
    """
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        parent_link=True,
    )
    file = models.FileField(
        verbose_name="Arquivo",
        upload_to=settings.PDF_ARTIFACT_DIR,
    )

    class Meta:
        verbose_name = "Documento PDF"
        verbose_name_plural = "Documentos PDF"


class ImageDocument(Document):
    """
    Uma imagem
    """
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        parent_link=True,
    )
    file = models.FileField(
        verbose_name="Arquivo",
        upload_to=settings.IMAGE_ARTIFACT_DIR,
    )

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"
