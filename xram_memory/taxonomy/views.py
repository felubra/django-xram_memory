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
from xram_memory.artifact.models import News
from xram_memory.lib.stopwords import stopwords
from django.db.models import Prefetch, Q
import re
import string
from natsort import natsorted
from django.db.models.functions import Lower

# Create your views here.

TIMEOUT = 0 if settings.DEBUG else 60 * 60 * 12

class KeywordViewSet(viewsets.ViewSet):
    def top_keywords(self, request):
        pt_stopwords = stopwords.get("pt", [])

        max_keywords = request.GET.get("max", "250")
        if not max_keywords or not max_keywords.isnumeric():
            raise ParseError()

        max_keywords = int(max_keywords, 10)
        if max_keywords < 1:
            raise ValueError()

        keywords_list = (
            Keyword.objects
            .values("name", "slug")
            .annotate(name_lower=Lower("name") )
            .annotate(news_count=Count('news'))
            .filter(
                Q(news_count__gt=0)
            )
            .prefetch_related(
                Prefetch('news_set', queryset=News.objects.filter(published=True))
            )
            .exclude(name_lower__in=pt_stopwords)
            .order_by("-news_count")
            [:max_keywords]
        )
        return Response(keywords_list)

    def artifacts_for_keyword(self, request, keyword_slug):
        queryset = Keyword.objects.all()
        keyword = get_object_or_404(queryset, slug=keyword_slug)
        serialized_news = ArtifactSerializer(keyword.news, many=True)
        serialized_documents = ArtifactSerializer(keyword.document, many=True)
        return Response(serialized_news.data + serialized_documents.data)


class SubjectViewSet(viewsets.ViewSet):
    QUERY_INITIAL_REGEX = re.compile(r"^[a-zA-Z!]$")
    QUERY_LIMIT_REGEX = re.compile(r"^\d+$")

    def subjects_by_initial(self, request, initial=None):
        """
        Retorna uma lista com todos os assuntos, dada uma letra inicial.
        """
        if not initial or not self.QUERY_INITIAL_REGEX.match(initial):
            raise ParseError()
        if initial == '!':
            queryset = (
                Subject.objects
                .exclude(slug__regex=r'^[a-zA-Z]')
            )
        else:
            queryset = (
                Subject.objects
                .filter(slug__istartswith=initial)
            )


        subjects = natsorted(list(queryset), lambda subject: subject.slug.lower())
        serializer = SimpleSubjectSerializer(subjects, many=True)
        return Response(serializer.data)

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
            subjects = list(random_featured_subjects)
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)
        raise ParseError()

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
