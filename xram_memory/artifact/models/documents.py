import magic
from pathlib import Path
from django.core.files.base import ContentFile, File

from django.conf import settings
from django.db import models
from .artifact import Artifact
from django_rq import job

from xram_memory.utils import FileValidator
from easy_thumbnails.fields import ThumbnailerField


def get_file_path(instance, filename):
    """
    Tenta salvar os arquivos em locais diferentes para tipos de arquivo diferentes e dar um prefixo
    para um arquivo criado pelo usuário.
    """
    # Se esta é uma instância de ContentFile, extraia o mime type aqui
    if isinstance(instance.file.file, ContentFile):
        mime_type = magic.from_buffer(instance.file.file.read(1024), mime=True)
    # senão, tente contar com o mime type inserido pela função validadora
    else:
        mime_type = getattr(instance.file.file, '_mime_type', '')

    # adicione um prefixo no arquivo se um usuário criou ele
    file_prefix = 'u_{user_id}'.format(
        user_id=instance.created_by.id) if instance.is_user_object else ''

    # salve cada arquivo de acordo com o seu mimetype, se disponível
    if 'image/' in mime_type:
        folder_name = getattr(settings, 'IMAGE_ARTIFACT_DIR', '')
    elif mime_type == 'application/pdf':
        folder_name = getattr(settings, 'PDF_ARTIFACT_DIR', '')
    else:
        folder_name = ''

    return '{folder_name}{file_prefix}_{filename}'.format(file_prefix=file_prefix, folder_name=folder_name, filename=filename)


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
    file = ThumbnailerField(
        verbose_name="Arquivo",
        upload_to=get_file_path,
        # TODO: Considerar alterar o validador em si, pois qualquer alteração na lista de mimes requer uma nova migração
        validators=[FileValidator(
            content_types=settings.VALID_FILE_UPLOAD_MIME_TYPES)],
    )

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
            self.mime_type = magic.from_buffer(
                self.file.read(1024), mime=True)
        except:
            self.mime_type = ''

    def determine_file_size(self):
        try:
            self.file_size = self.file.size
        except:
            self.file_size = '0'
