from xram_memory.artifact.models import Artifact, News, Document
from django.test import TestCase, Client, TransactionTestCase
from xram_memory.artifact.news_fetcher import NewsFetcher
from django.template.response import TemplateResponse
from django.contrib.admin.options import ModelAdmin
from django.template.defaultfilters import slugify
from xram_memory.artifact.admin import NewsAdmin
from django.contrib.admin.sites import AdminSite
from xram_memory.taxonomy.models import Keyword
from xram_memory.users.models import User
from xram_memory.lib import stopwords
from django.db import transaction
import newspaper as newspaper3k
from django.urls import reverse
from loguru import logger
from pathlib import Path
import requests_mock
import requests
import logging
import os

logger.remove()

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
