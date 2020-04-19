from xram_memory.artifact.serializers import DocumentSerializer, NewsSerializer, PhotoAlbumFolderSerializer, SimplePhotoAlbumFolderSerializer
from xram_memory.artifact.models import Document, News
from django.shortcuts import get_object_or_404
from boltons.cacheutils import cachedproperty
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from filer.models import Folder, File
from hashid_field.rest import Hashid
from rest_framework import viewsets
from django.db.models import Count
from django.conf import settings
from django.http import Http404


class DocumentViewSet(viewsets.ViewSet):
    """
    Lista os documentos públicos
    """

    def retrieve(self, request, document_id=None):
        queryset = Document.objects.filter(is_public=True)
        document = get_object_or_404(queryset, document_id=document_id)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)


class NewsViewSet(viewsets.ViewSet):
    """
    Lista as notícias publicadas
    """

    def retrieve(self, request, slug=None):
        queryset = News.objects.filter(published=True)
        news = get_object_or_404(queryset, slug=slug)
        serializer = NewsSerializer(news)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ViewSet):
    # TODO: filtrar, pelo mimetype, os arquivos das pastas para apenas retornar imagens
    # TODO: prever caso em que teremos que limpar este cache
    @cachedproperty
    def _main_photoalbums_folder(self):
        return Folder.objects.get(
            name=settings.FOLDER_PHOTO_ALBUMS['name'])

    def listing(self, request):
        """
        Lista os álbuns, ou seja, uma pasta que é subpasta da pasta 'Álbuns de fotos'
        """
        photo_albums_folder = self._main_photoalbums_folder
        queryset = Folder.objects.annotate(num_files=Count("all_files")).filter(
            parent=photo_albums_folder, num_files__gt=0).order_by("-modified_at")
        albums = list(queryset)
        serializer = SimplePhotoAlbumFolderSerializer(albums, many=True)
        return Response(serializer.data)

    def retrieve(self, request, album_id=None):
        """
        Retorna um álbum com as fotos
        """

        try:
            hashid = Hashid(album_id, settings.HASHID_FIELD_SALT, 7)
            pk = hashid.id
            try:
                int_album_id = int(album_id)
            except:
                pass
            else:
                # Não permita a tentativa de acesso pelo id numérico e interno (id)
                if (pk == int_album_id):
                    raise ValueError(
                        "Usuário tentou acessar o álbum por número interno")
        except ValueError:
            raise Http404()

        photo_albums_folder = self._main_photoalbums_folder
        queryset = Folder.objects.annotate(num_files=Count("all_files")).filter(
            parent=photo_albums_folder, num_files__gt=0, pk=pk)
        album = get_object_or_404(queryset)
        serializer = PhotoAlbumFolderSerializer(album)
        return Response(serializer.data)
