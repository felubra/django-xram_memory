from .serializers import StaticPageSerializer, SimpleStaticPageSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from .models import StaticPage


# TODO: Fazer o rate limit desses endpoints: https://www.django-rest-framework.org/api-guide/throttling/


class InMenuStaticPagesViewSet(viewsets.ViewSet):
    """Uma view para uma lista com páginas que devem ter links no menu principal"""

    def listing(self, request):
        queryset = StaticPage.objects.filter(
            published=True, show_in_menu=True).order_by('-modified_at')
        pages = get_list_or_404(queryset)
        serializer = SimpleStaticPageSerializer(pages, many=True)
        return Response(serializer.data)


class FeaturedStaticPagesViewSet(viewsets.ViewSet):
    """Uma view para uma lista com páginas que devem aparecer como blocos de chamada na página
    inicial"""

    def listing(self, request):
        queryset = StaticPage.objects.filter(
            published=True, featured=True).order_by('-modified_at')
        pages = get_list_or_404(queryset)
        serializer = SimpleStaticPageSerializer(pages, many=True)
        return Response(serializer.data)


class StaticPageViewSet(viewsets.ViewSet):
    """Um endpoint pegar uma página"""

    def retrieve(self, request, pk=None):
        queryset = StaticPage.objects.filter(published=True)
        page = get_object_or_404(queryset, pk=pk)
        serializer = StaticPageSerializer(page)
        return Response(serializer.data)
