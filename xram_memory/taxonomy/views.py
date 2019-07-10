from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from .serializers import SubjectSerializer
from django.db.models import Subquery
from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework import viewsets
from .models import Subject

# Create your views here.


class SubjectViewSet(viewsets.ViewSet):

    # @method_decorator(cache_page(60 * 60 * 12))
    def listing(self, request):
        """
        Retorna uma lista com dois assuntos aleatórios, usados na página 'Assuntos'.
        Essa lista deve mudar a cada 12 horas, conforme parâmetro de cache acima.
        """
        queryset = Subject.objects.filter(pk__in=Subquery(Subject.objects.filter(description__isnull=False).exclude(description__exact='').annotate(num_news=Count(
            'news'), num_documents=Count('document')).filter(Q(num_documents__gt=0) | Q(num_news__gt=0)).filter(news__image_capture__isnull=False).distinct().values('pk'))).order_by("?")[:2]

        subjects = get_list_or_404(queryset)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
