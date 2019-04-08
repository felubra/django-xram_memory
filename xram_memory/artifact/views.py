from xram_memory.artifact.serializers import DocumentSerializer, NewsSerializer, PhotoAlbumFolderSerializer, SimplePhotoAlbumFolderSerializer
from xram_memory.artifact.models import Document, News
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from filer.models import Folder, File
from rest_framework import viewsets
from django.conf import settings


class DocumentViewSet(viewsets.ViewSet):
    """
    Lista os documentos públicos
    """

    def retrieve(self, request, pk=None):
        queryset = Document.objects.filter(is_public=True)
        document = get_object_or_404(queryset, pk=pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)


class NewsViewSet(viewsets.ViewSet):
    """
    Lista as notícias publicadas
    """

    def retrieve(self, request, pk=None):
        queryset = News.objects.filter(published=True)
        news = get_object_or_404(queryset, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ViewSet):
    def listing(self, request):
        """
        Lista os álbuns, ou seja, uma pasta que é subpasta da pasta 'Álbuns de fotos'
        """
        photo_albums_folder = Folder.objects.get(
            name=settings.FOLDER_PHOTO_ALBUMS['name'])
        queryset = Folder.objects.filter(
            parent=photo_albums_folder).order_by("-modified_at")
        albums = get_list_or_404(queryset)
        serializer = SimplePhotoAlbumFolderSerializer(albums, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retorna um álbum com as fotos
        """
        photo_albuns_folder = Folder.objects.get(
            name=settings.FOLDER_PHOTO_ALBUMS['name'])
        queryset = Folder.objects.filter(
            parent=photo_albuns_folder, pk=pk)
        album = get_object_or_404(queryset)
        serializer = PhotoAlbumFolderSerializer(album)
        return Response(serializer.data)
