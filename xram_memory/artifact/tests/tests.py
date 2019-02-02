import os
import logging
from pathlib import Path

import requests
import requests_mock
import newspaper as newspaper3k

from django.test import TestCase, Client, TransactionTestCase
from django.template.defaultfilters import slugify
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.urls import reverse
from django.db import transaction
from django.template.response import TemplateResponse


from xram_memory.users.models import User
from xram_memory.taxonomy.models import Keyword

from xram_memory.artifact.models import Artifact, News, Document
from xram_memory.artifact.admin import NewsAdmin

from xram_memory.artifact.news_fetcher import NewsFetcher
from xram_memory.lib import stopwords

logger = logging.getLogger(__name__)

# Create your tests here.


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class NewsTestCase(TestCase):

    def test_create_without_url(self):
        artifact = News(title="Abacate")
        self.assertRaises(ValueError, artifact.save)

    def test_create_without_title(self):
        # Se colocássemos uma url válida, existiria a possibilidade do título ser preenchido automaticamente
        artifact = News(url="https://does-not-exists998.com")
        self.assertRaises(ValueError, artifact.save)


class NewsAdminFormTestCase(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        self.automatic_news = News(
            url="https://politica.estadao.com.br/noticias/geral,em-diplomacao-bolsonaro-diz-que-a-soberania-do-voto-popular-e-inquebrantavel,70002640605")
        self.site = AdminSite()
        self.user_info = {
            'username': 'admin',
            'email': 'test@test.com',
            'password': 'test@test.com'
        }
        self.user = User.objects.create_superuser(**self.user_info)
        self.client = Client()
        self.client.login(**self.user_info)

    def test_fields_for_new_item(self):
        """Testa a presença/ausência e os valores dos campos quando em modo de inserção"""
        response: TemplateResponse = self.client.get(reverse(
            "admin:artifact_news_add"))
        self.assertEqual(response.status_code, 200)

        admin_form = response.context_data['adminform']
        # Deverão existir quatro grupos de campos...
        self.assertEqual(len(admin_form.fieldsets), 4)
        # Um desses precisa se chamar 'Avançado'

    def test_fields_for_existing_item(self):
        """Testa a presença/ausência e os valores dos campos quando em modo de edição"""
        self.automatic_news.save()

        response: TemplateResponse = self.client.get(reverse(
            "admin:artifact_news_change", args=[self.automatic_news.pk]))
        self.assertEqual(response.status_code, 200)

        admin_form = response.context_data['adminform']
        # Deverão existir três grupos de campos...
        self.assertEqual(len(admin_form.fieldsets), 5)
        # Um desses precisa se chamar 'Avançado'


@requests_mock.Mocker()
class NewsFetcherTestCase(TestCase):

    def setUp(self):
        with open(str(Path(os.path.dirname(__file__), 'mocks', '0.html')), encoding='utf-8') as f:
            self.article_content = f.read()

    def test_fetch_basic_basic_fields(self, m):
        BASIC_FIELDS = ['title', 'image', 'body', 'teaser',
                        'published_date', 'authors', 'keywords', 'language']

        article_url = "https://politica.estadao.com.br/blogs/fausto-macedo/justica-decreta-bloqueio-de-r-5-bilhoes/"
        m.register_uri('GET', article_url,
                       text=self.article_content)

        basic_info = NewsFetcher.fetch_basic_info(
            article_url, fetch_images=False)
        for field in BASIC_FIELDS:
            self.assertIn(field, basic_info)

    def test_fetch_basic_basic_no_stopword_keyword(self, m):
        article_url = "https://politica.estadao.com.br/blogs/fausto-macedo/justica-decreta-bloqueio-de-r-5-bilhoes/"
        m.register_uri('GET', article_url,
                       text=self.article_content)

        basic_info = NewsFetcher.fetch_basic_info(
            article_url, fetch_images=False)
        self.assertEqual(basic_info["language"], "pt")
        for keyword in basic_info["keywords"]:
            self.assertNotIn(keyword, stopwords["pt"])
