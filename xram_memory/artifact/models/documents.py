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
        max_length=255, blank=True, editable=False, help_text="Tipo do arquivo")
    file_size = models.fields.PositiveIntegerField(
        default=0, editable=False, help_text="Tamanho do arquivo em bytes")
    is_user_object = models.BooleanField(verbose_name="Objeto criado pelo usuário?", editable=False,
                                         default=True, help_text="Indica se o arquivo foi inserido diretamente por um usuário")
    file = NotImplemented

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.title

    @job
    def extract_additional_info(self):
        """
        Com base no mimetype do arquivo, tenta extrair informações adicionais e salvá-las serializadas como JSON no
        campo `additional_info`
        """
        pass

    def save(self, *args, **kwargs):
        self.size = self.file.size
        if not self.title:
            self.title = self.file.name
        super(Document, self).save(*args, **kwargs)

    def determine_mime_type(self):
        try:
            self.mime_type = magic.from_file(self.file.path, mime=True)
        except Exception as err:
            self.mime_type = ''


class PDFDocument(Document):
    """
    Um documento PDF
    """
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, parent_link=True)
    file = models.FileField(
        verbose_name="Arquivo", upload_to=settings.PDF_ARTIFACT_DIR)

    class Meta:
        verbose_name = "Documento PDF"
        verbose_name_plural = "Documentos PDF"


class ImageDocument(Document):
    """
    Uma imagem
    """
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, parent_link=True)
    file = models.FileField(
        verbose_name="Arquivo", upload_to=settings.IMAGE_ARTIFACT_DIR)

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"
