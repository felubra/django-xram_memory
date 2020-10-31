from .serializers import SubjectSerializer, SimpleSubjectSerializer, KeywordSerializer
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
from xram_memory.artifact.serializers import ArtifactSerializer
from .models import Subject, Keyword
from xram_memory.artifact.models import News, Document
from xram_memory.lib.stopwords import stopwords
from django.db.models import Prefetch, Q
import re
import string
from natsort import natsorted
from django.db.models.functions import Lower

# Create your views here.

TIMEOUT = 0 if settings.DEBUG else 60 * 60 * 12

class KeywordViewSet(viewsets.ViewSet):
    def listing(self, request):
        # Pegue uma lista com as stopwords em pt-br
        pt_stopwords = stopwords.get("pt", [])
        # Pegue e valide o parâmetro com o máximo de itens a retornar
        max_keywords = request.GET.get("max", "250")
        if not max_keywords or not max_keywords.isnumeric():
            raise ParseError()
        max_keywords = int(max_keywords, 10)
        if max_keywords < 1:
            raise ValueError()

        queryset = (Keyword.objects
                    .values("name", "slug")
                    .annotate(name_lower=Lower("name") )
                    .annotate(news_count=Count('news'))
                    .filter(
                        Q(news_count__gt=0)
                    )
                    .prefetch_related(
                        Prefetch('news_set', queryset=News.objects.filter(published=True))
                    )
                    .exclude(name_lower__in=pt_stopwords))

        order_by = self.request.query_params.get('orderBy', None)
        if order_by is not None:
            if order_by == 'top':
                queryset = queryset .order_by("-news_count")
            else:
                raise ParseError()

        return Response(queryset[:max_keywords])

    def artifacts_for_keyword(self, request, keyword_slug):
        queryset = Keyword.objects.all()
        keyword = get_object_or_404(queryset, slug=keyword_slug)
        serialized_news = ArtifactSerializer(keyword.news, many=True)
        serialized_documents = ArtifactSerializer(keyword.document, many=True)
        return Response(serialized_news.data + serialized_documents.data)


class SubjectViewSet(viewsets.ViewSet):
    QUERY_INITIAL_REGEX = re.compile(r"^[a-zA-Z!]$")
    QUERY_LIMIT_REGEX = re.compile(r"^\d+$")

    def listing(self, request):
        limit = self.request.query_params.get('limit', None)
        filter_by = self.request.query_params.get('filterBy', None)
        initial = self.request.query_params.get('initial', None)
        if (limit is None) or self.QUERY_LIMIT_REGEX.match(limit):
            ChosenSerializer = SimpleSubjectSerializer
            queryset = (Subject.objects
                .all()
                .annotate(news_count=Count('news'))
                .annotate(document_count=Count('document'))
                .prefetch_related(
                    Prefetch('news', queryset=News.objects.filter(published=True)),
                    Prefetch('document', queryset=Document.objects.filter(is_public=True))
                )
                .filter(
                    Q(news_count__gt=0)
                    |
                    Q(document_count__gt=0)
                )
            )
            if filter_by is not None:
                if filter_by == 'featured':
                    queryset = (queryset
                                    .filter(featured=True).order_by("?")
                                    .prefetch_related('news',
                                        Prefetch('news__image_capture__image_document'),
                                    )
                    )
                    # Utilize o outro serializador, que trás as imagens e é mais demorado
                    # para o caso dos assuntos em destaque
                    ChosenSerializer = SubjectSerializer
            if initial is not None:
                queryset = self._subjects_by_initial(initial)
            if limit is not None:
                queryset = queryset[:int(limit)]
            serializer = ChosenSerializer(queryset, many=True)
            return Response(serializer.data)
        raise ParseError()

    def _subjects_by_initial(self, initial=None):
        """
        Retorna uma lista com todos os assuntos, dada uma letra inicial.
        """
        if not initial or not self.QUERY_INITIAL_REGEX.match(initial):
            raise ParseError()
        if initial == '!':
            return (
                Subject.objects
                .exclude(slug__regex=r'^[a-zA-Z]')
            )
        else:
            return (
                Subject.objects
                .filter(slug__istartswith=initial)
            )

    def subjects_initials(self, request):
        initials = []
        INITIALS_FILTER = '!' + string.ascii_uppercase

        for initial in INITIALS_FILTER:
            if initial == '!':
                results = Subject.objects.exclude(slug__regex=r'^[a-zA-Z]')
            else:
                results = Subject.objects.filter(slug__istartswith=initial)
            if results.count() > 0:
                initials.append(initial)

        return Response(initials)

    def retrieve(self, request, subject_slug=None):
        queryset = Subject.objects.all()
        subject = get_object_or_404(queryset, slug=subject_slug)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def artifacts_for_subject(self, request, subject_slug):
        queryset = Subject.objects.all()
        subject = get_object_or_404(queryset, slug=subject_slug)
        serialized_news = ArtifactSerializer(subject.news, many=True)
        serialized_documents = ArtifactSerializer(subject.document, many=True)
        return Response(serialized_news.data + serialized_documents.data)
