from xram_memory.artifact.models import Artifact, News, Document
from django.test import TestCase, Client, TransactionTestCase
from django.template.response import TemplateResponse
from django.contrib.admin.options import ModelAdmin
from django.template.defaultfilters import slugify
from xram_memory.artifact.admin import NewsAdmin
from django.contrib.admin.sites import AdminSite
from xram_memory.taxonomy.models import Keyword
from xram_memory.lib.stopwords import stopwords
from xram_memory.users.models import User
from xram_memory.lib import NewsFetcher
from django.db import transaction
import newspaper as newspaper3k
from django.urls import reverse
from loguru import logger
from pathlib import Path
import requests_mock
import requests
import os


logger.remove()


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
