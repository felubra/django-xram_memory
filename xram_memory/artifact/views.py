from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from filer.models import File
from xram_memory.artifact.models import News
from xram_memory.artifact.serializers import DocumentSerializer, NewsSerializer

# TODO: Fazer o rate limit desses endpoints: https://www.django-rest-framework.org/api-guide/throttling/


class DocumentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def retrieve(self, request, pk=None):
        queryset = File.objects.filter(is_public=True)
        document = get_object_or_404(queryset, pk=pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)


class NewsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def retrieve(self, request, pk=None):
        queryset = News.objects.filter(published=True)
        news = get_object_or_404(queryset, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
