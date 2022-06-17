from django.db import models
from filer.models.foldermodels import Folder
from filer.fields.file import FilerFileField
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


def is_album_folder(folder):
    # veririca se uma dada pasta é uma pasta de álbum, ela é se é uma subpasta da pasta de álbuns
    if folder.parent:
        return folder.parent.id == settings.FOLDER_PHOTO_ALBUMS["id"]
    return False


# TODO: Adicionar funcionalidades outrora implementadas em PhotoAlbumFolderSerializer
class Album(models.Model):
    folder = models.OneToOneField(
        Folder, related_name="album", on_delete=models.CASCADE, primary_key=True
    )

    # Campos para enriquecer uma pasta-álbum de fotos
    featured = models.BooleanField("Em destaque na página de álbums", default=True)
    description = models.TextField(
        verbose_name="Descrição", help_text="Uma descrição para este Álbum", blank=True
    )
    cover = FilerFileField(
        null=True, blank=True, related_name="album_cover", on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Álbum de foto"
        verbose_name = "Álbuns de fotos"

    def __str__(self):
        return self.folder.name


@receiver(post_save, sender=Folder)
def create_album_folder(sender, instance, created, **kwargs):
    # Na criação de uma subpasta da pasta álbums de fotos, crie um álbum e o associe à pasta criada
    if created and is_album_folder(instance):
        Album.objects.create(folder=instance)


@receiver(post_save, sender=Folder)
def save_album_folder(sender, instance, **kwargs):
    # Salve o álbum associado quando salvarmos a pasta
    try:
        instance.album.save()
    except Album.DoesNotExist:
        # Se a pasta é uma pasta de álbum, mas não existe um associado, crie-o agora.
        if is_album_folder(instance):
            Album.objects.create(folder=instance)
