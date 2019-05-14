from django.test import TestCase, Client, TransactionTestCase
from django.contrib.admin.options import ModelAdmin
from xram_memory.artifact.models import Newspaper
from django.contrib.admin.sites import AdminSite
from xram_memory.lib import NewsFetcher
from contextlib import contextmanager
from django.urls import reverse
from unittest import mock
from loguru import logger
import favicon

logger.remove()

BOGUS_NEWSPAPER = mock.Mock(
    description="Um jornaleco de nada", brand="jornaleco")


class NewspaperEssentialTests(TestCase):
    @contextmanager
    def minimal_newspaper(self):
        yield Newspaper(url="https://www.folha.uol.com.br/")

    def test_has_basic_info(self):
        with self.minimal_newspaper() as newspaper:
            self.assertFalse(newspaper.has_basic_info)

            newspaper.title = newspaper.url
            self.assertFalse(newspaper.has_basic_info)

            newspaper.title = "Folha de São Paulo"
            self.assertTrue(newspaper.has_basic_info)

    def test_has_basic_info2(self):
        with self.minimal_newspaper() as newspaper:
            with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
                newspaper.set_basic_info()
                self.assertTrue(newspaper.has_basic_info)

    def test_has_logo(self):
        with self.minimal_newspaper() as newspaper:
            self.assertFalse(newspaper.has_logo)
            newspaper.save()
            self.assertFalse(newspaper.has_logo)

    def test_string_value(self):
        with self.minimal_newspaper() as newspaper:
            self.assertEqual(str(newspaper), '(site sem título)')
            with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
                newspaper.set_basic_info()
                self.assertEqual(str(newspaper), BOGUS_NEWSPAPER.brand)

    def test_initial_flags_state(self):
        newspaper = Newspaper()
        self.assertFalse(newspaper.has_basic_info)
        self.assertFalse(newspaper.has_logo)
        self.assertEqual(newspaper.favicon_logo, '')

    def test_set_logo_from_favicon(self):
        with self.minimal_newspaper() as newspaper:
            result = newspaper.set_logo_from_favicon()
            self.assertTrue(result)
            self.assertTrue(newspaper.has_logo)
            self.assertNotEqual(newspaper.favicon_logo, '')
            logo_filename = newspaper.logo.file.name
            result = newspaper.set_logo_from_favicon()
            self.assertTrue(result)
            self.assertNotEqual(logo_filename, newspaper.logo.file.name)
            with mock.patch.object(favicon, 'get') as affected_function:
                affected_function.return_value = []
                result = newspaper.set_logo_from_favicon()
                self.assertFalse(result)
