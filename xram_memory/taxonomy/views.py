from .serializers import SubjectSerializer, SimpleSubjectSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from django.db.models import Subquery
from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework import viewsets
from django.conf import settings
from .models import Subject
import re
import string

# Create your views here.

TIMEOUT = 0 if settings.DEBUG else 60 * 60 * 12


class SubjectViewSet(viewsets.ViewSet):
    QUERY_INITIAL_REGEX = re.compile('^[a-zA-Z]$')
    QUERY_LIMIT_REGEX = re.compile('^\d+$')

    @method_decorator(cache_page(TIMEOUT))
    def subjects_by_initial(self, request, initial=None):
        """
        Retorna uma lista com todos os assuntos, dada uma letra inicial.
        """
        if not initial or not self.QUERY_INITIAL_REGEX.match(initial):
            raise ParseError()
        queryset = Subject.objects.filter(
            name__startswith=initial).order_by('name')

        subjects = get_list_or_404(queryset)
        serializer = SimpleSubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(TIMEOUT))
    def subjects_initials(self, request):
        initials = []
        INITIALS_FILTER = '#' + string.ascii_uppercase

        for filter in INITIALS_FILTER:
            if filter is '#':
                results = Subject.objects.exclude(name__regex=r'^[a-zA-Z]')
            else:
                results = Subject.objects.filter(name__istartswith=filter)
            if results.count():
                initials.append(filter)

        return Response(initials)

    @method_decorator(cache_page(TIMEOUT))
    def featured(self, request):
        """
        Retorna uma lista aleatória com assuntos em destaque, de acordo com a quantidade estipulada
        pelo cliente.
        """
        limit = self.request.query_params.get('limit', '5')
        if self.QUERY_LIMIT_REGEX.match(limit):
            limit = int(limit)
            random_featured_subjects = Subject.objects.filter(
                featured=True).order_by("?")[:limit]
            subjects = get_list_or_404(random_featured_subjects)
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)
        raise ParseError()

    def retrieve(self, request, subject_slug=None):
        queryset = Subject.objects.all()
        subject = get_object_or_404(queryset, slug=subject_slug)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)
