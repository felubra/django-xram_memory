from django.db import models
from xram_memory.taxonomy.models import Subject, Keyword
from filer.models.foldermodels import Folder
from filer.fields.file import FilerFileField

# Create your models here.


# TODO: Adicionar funcionalidades outrora implementadas em PhotoAlbumFolderSerializer
class Album(models.Model):
    folder = models.OneToOneField(
        Folder, related_name="album", on_delete=models.CASCADE)

    # Campos para enriquecer uma pasta-álbum de fotos
    featured = models.BooleanField(
        "Em destaque na página de álbums", default=True)
    description = models.TextField(
        verbose_name="Descrição",
        help_text='Uma descrição para este Álbum',
        blank=True)
    cover = FilerFileField(
        null=True, blank=True, related_name="album_cover", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Álbum de foto"
        verbose_name = "Álbuns de fotos"

    def __str__(self):
        return self.folder.name
