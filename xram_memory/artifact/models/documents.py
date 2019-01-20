import magic

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
    file_hash = models.CharField(blank=True, editable=False,
                                 max_length=32, help_text="Hash único do arquivo em MD5")
    additional_info = models.TextField(
        null=True, editable=False, help_text="Informações adicionais sobre o arquivo (JSON)")
    is_user_object = models.BooleanField(
        default=True, help_text="Indica se o arquivo foi inserido diretamente por um usuário")

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        if not self.additional_info:
            # TODO: fazer um decorador, abstrair o padrão abaixo de tentar executar assíncronamente mas executar
            # síncronamente se o redis não estiver disponível. Logar em caso de erro.
            try:
                self.extract_additional_info.delay()
            except:
                self.extract_additional_info()

    @job
    def extract_additional_info(self):
        """
        Com base no mimetype do arquivo, tenta extrair informações adicionais e salvá-las serializadas como JSON no
        campo `additional_info`
        """
        pass


class PDFDocument(Document):
    """
    Um documento PDF
    """
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, parent_link=True)
    pdf_file = models.FileField(
        verbose_name="Arquivo", upload_to=settings.PDF_ARTIFACT_DIR)

    class Meta:
        verbose_name = "Documento PDF"
        verbose_name_plural = "Documentos PDF"

    def save(self, *args, **kwargs):
        self.determine_mime_type()
        if not self.title:
            try:
                self.title = self.pdf_file.name
            except:
                self.title = "Documento PDF {}".format(self.id)
        super(PDFDocument, self).save(*args, **kwargs)

    def determine_mime_type(self):
        try:
            self.mime_type = magic.from_file(self.pdf_file.path, mime=True)
        except:
            self.mime_type = 'application/pdf'


class ImageDocument(Document):
    """
    Uma imagem
    """
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, parent_link=True)
    image_file = models.FileField(
        verbose_name="Arquivo", upload_to=settings.IMAGE_ARTIFACT_DIR)

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"

    def save(self, *args, **kwargs):
        self.determine_mime_type()
        if not self.title:
            try:
                self.title = self.image_file.name
            except:
                self.title = "Documento de Imagem {}".format(self.id)
        super(ImageDocument, self).save(*args, **kwargs)

    def determine_mime_type(self):
        try:
            self.mime_type = magic.from_file(self.image_file.name, mime=True)
        except:
            self.mime_type = ''
