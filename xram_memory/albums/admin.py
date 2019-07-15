from django.contrib import admin
from .models import Album
from filer.models.foldermodels import Folder
from filer.admin.folderadmin import FolderAdmin
from django.conf import settings
from django import forms
from xram_memory.artifact.models import Document


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['cover'].queryset = Document.objects.filter(
                mime_type__startswith="image/")


class AlbumInline(admin.StackedInline):
    model = Album
    can_delete = False
    max_num = 1
    extra = 0
    verbose_name_plural = 'Álbum de foto'
    template = "admin/albums/album/edit_inline/stacked.html"
    form = AlbumForm


class AlbumAdmin(FolderAdmin):
    inlines = [AlbumInline, ]

    def get_inline_instances(self, request, obj=None):
        to_return = super().get_inline_instances(request, obj)
        # filter out the RelativeInlines if obj.is_member is false

        if obj.parent.id != settings.FOLDER_PHOTO_ALBUMS['id']:
            to_return = [
                x for x in to_return if not isinstance(x, AlbumInline)]
        return to_return


admin.site.unregister(Folder)
admin.site.register(Folder, AlbumAdmin)
