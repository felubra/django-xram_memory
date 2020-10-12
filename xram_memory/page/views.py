from .serializers import StaticPageSerializer, SimpleStaticPageSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from .models import StaticPage
from rest_framework.exceptions import ParseError


# TODO: Fazer o rate limit desses endpoints: https://www.django-rest-framework.org/api-guide/throttling/
class StaticPagesViewSet(viewsets.ViewSet):
    def listing(self, request):
        queryset = StaticPage.objects.filter(
            published=True).order_by('-modified_at')
        filter_by = self.request.query_params.get('filterBy', None)
        if filter_by is not None:
            if filter_by == 'featured':
                queryset = queryset.filter(featured=True)
            elif filter_by == 'in_menu':
                queryset = queryset.filter(show_in_menu=True)
            else:
                raise ParseError("Filtro inválido")
        pages = list(queryset)
        serializer = SimpleStaticPageSerializer(pages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, url=None):
        queryset = StaticPage.objects.filter(published=True)
        page = get_object_or_404(queryset, url=url)
        serializer = StaticPageSerializer(page)
        return Response(serializer.data)
