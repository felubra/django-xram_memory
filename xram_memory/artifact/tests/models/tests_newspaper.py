from django.test import TestCase, Client, TransactionTestCase
from django.contrib.admin.options import ModelAdmin
from xram_memory.artifact.models import Newspaper
from django.contrib.admin.sites import AdminSite
from django.db.models.signals import post_save
from xram_memory.lib import NewsFetcher
from contextlib import contextmanager
from dataclasses import dataclass
from django.urls import reverse
from loguru import logger
from unittest import mock
import requests_mock
import favicon
import factory
import pytest

logger.remove()

BOGUS_NEWSPAPER = mock.Mock(
    description="Um jornaleco de nada", brand="jornaleco")


@dataclass
class Favicon():
    format: str
    url: str


@contextmanager
def minimal_newspaper():
    yield Newspaper(url="https://www.folha.uol.com.br/")


def test_has_basic_info():
    with minimal_newspaper() as newspaper:
        assert newspaper.has_basic_info == False

        newspaper.title = newspaper.url
        assert newspaper.has_basic_info == False

        newspaper.title = "Folha de São Paulo"
        assert newspaper.has_basic_info == True


def test_has_basic_info2():
    with minimal_newspaper() as newspaper:
        with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
            newspaper.set_basic_info()
            assert newspaper.has_basic_info == True


@factory.django.mute_signals(post_save)
@pytest.mark.django_db(transaction=True)
def test_has_logo_after_save():
    with minimal_newspaper() as newspaper:
        assert newspaper.has_logo == False
        newspaper.save()
        assert newspaper.has_logo == False


def test_string_value():
    with minimal_newspaper() as newspaper:
        assert str(newspaper) == '(site sem título)'
        with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
            newspaper.set_basic_info()
            assert str(newspaper) == BOGUS_NEWSPAPER.brand


def test_initial_flags_state():
    newspaper = Newspaper()
    assert newspaper.has_basic_info == False
    assert newspaper.has_logo == False
    assert newspaper.favicon_logo == ''


def test_set_logo_from_favicon_without_a_saved_instance(shared_datadir):
    with minimal_newspaper() as newspaper:
        result = newspaper.set_logo_from_favicon()
        assert result == False
        assert newspaper.has_logo == False


@pytest.mark.django_db(transaction=True)
@factory.django.mute_signals(post_save)
def test_set_logo_from_favicon(shared_datadir):
    with minimal_newspaper() as newspaper:
        newspaper.save()
        contents = (shared_datadir / 'newspaper_favicon.png')
        with open(str(contents), 'rb') as f:
            with mock.patch.object(favicon, 'get') as mocked:
                mocked.return_value = [
                    Favicon(url='http://example.com/icon.gif', format='gif')]
                with requests_mock.Mocker() as m:
                    m.register_uri('GET', 'http://example.com/icon.gif',
                                   content=f.read())
                    result = newspaper.set_logo_from_favicon()
                    assert result == True
                    assert newspaper.has_logo == True
                    assert newspaper.favicon_logo != ''
                    result = newspaper.set_logo_from_favicon()
                    assert result == True
                    assert newspaper.has_logo == True
                    assert newspaper.favicon_logo != ''


@pytest.mark.django_db(transaction=True)
@factory.django.mute_signals(post_save)
def test_set_logo_from_favicon_no_favicons():
    with minimal_newspaper() as newspaper:
        newspaper.save()
        with mock.patch.object(favicon, 'get') as affected_function:
            affected_function.return_value = []
            result = newspaper.set_logo_from_favicon()
            assert result == False
