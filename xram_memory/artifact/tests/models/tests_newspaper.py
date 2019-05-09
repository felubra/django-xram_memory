from django.test import TestCase, Client, TransactionTestCase
from xram_memory.artifact.news_fetcher import NewsFetcher
from django.contrib.admin.options import ModelAdmin
from xram_memory.artifact.models import Newspaper
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from unittest import mock
from loguru import logger

logger.remove()

BOGUS_NEWSPAPER = mock.Mock(
    description="Um jornaleco de nada", brand="jornaleco")


class NewspaperEssentialTests(TestCase):
    def init_mininal(self):
        return Newspaper(url="https://www.folha.uol.com.br/")

    def test_has_basic_info(self):
        newspaper = self.init_mininal()
        self.assertFalse(newspaper.has_basic_info)

        newspaper.title = newspaper.url
        self.assertFalse(newspaper.has_basic_info)

        newspaper.title = "Folha de São Paulo"
        self.assertTrue(newspaper.has_basic_info)

        with mock.patch('xram_memory.artifact.news_fetcher.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
            newspaper = self.init_mininal()
            # TODO: mockar NewsFetcher.build_newspaper
            newspaper.set_basic_info()
            self.assertTrue(newspaper.has_basic_info)

    def test_has_logo(self):
        newspaper = self.init_mininal()
        self.assertFalse(newspaper.has_logo)

        newspaper.save()
        self.assertFalse(newspaper.has_logo)
