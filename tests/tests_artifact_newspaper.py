from xram_memory.artifact.models import Newspaper
from django.db.models.signals import post_save
from contextlib import contextmanager
from dataclasses import dataclass
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
    """
    Verifica newspaper.has_basic_info com definição direta de propriedades
    """
    with minimal_newspaper() as newspaper:
        assert newspaper.has_basic_info == False

        newspaper.title = newspaper.url
        assert newspaper.has_basic_info == False

        newspaper.title = "Folha de São Paulo"
        assert newspaper.has_basic_info == True


def test_has_basic_info2():
    """
    Verifica newspaper.has_basic_info com o uso de set_basic_info()
    """
    with minimal_newspaper() as newspaper:
        with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
            assert newspaper.has_basic_info == False
            newspaper.set_basic_info()
            assert newspaper.has_basic_info == True


@factory.django.mute_signals(post_save)
@pytest.mark.django_db(transaction=True)
def test_has_logo_after_save():
    """
    Verifica se o logotipo do jornal é definido depois de seu salvamento
    """
    with minimal_newspaper() as newspaper:
        assert newspaper.has_logo == False
        newspaper.save()
        assert newspaper.has_logo == False


def test_string_value():
    """
    Verifica a implementação de Newspaper.__str__
    """
    with minimal_newspaper() as newspaper:
        assert str(newspaper) == '(site sem título)'
        with mock.patch('xram_memory.lib.NewsFetcher.build_newspaper', return_value=BOGUS_NEWSPAPER):
            newspaper.set_basic_info()
            assert str(newspaper) == BOGUS_NEWSPAPER.brand


def test_initial_flags_state():
    """
    Verifica o estado inicial de algumas flags e propriedades
    """
    newspaper = Newspaper()
    assert newspaper.has_basic_info == False
    assert newspaper.has_logo == False
    assert newspaper.favicon_logo == ''


def test_set_logo_from_favicon_without_a_saved_instance(shared_datadir):
    """
    Verifica se tentar definir um logo para uma instância não salva é rejeitado
    """
    with minimal_newspaper() as newspaper:
        result = newspaper.set_logo_from_favicon()
        assert result == False
        assert newspaper.has_logo == False


@pytest.mark.django_db(transaction=True)
@factory.django.mute_signals(post_save)
def test_set_logo_from_favicon(shared_datadir):
    """
    Testa set_logo_from_favicon() e newspaper.has_logo com logotipos obtidos
    """
    with minimal_newspaper() as newspaper:
        newspaper.save()
        contents = (shared_datadir / 'newspaper_favicon.png')
        with open(str(contents), 'rb') as f:
            with mock.patch.object(favicon, 'get') as mocked:
                mocked.return_value = [
                    Favicon(url='http://example.com/icon.gif', format='gif')]
                with requests_mock.Mocker() as m:
                    assert newspaper.has_logo == False
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
    """
    Testa set_logo_from_favicon() e newspaper.has_logo sem logotipos obtidos
    """
    with minimal_newspaper() as newspaper:
        newspaper.save()
        with mock.patch.object(favicon, 'get') as affected_function:
            affected_function.return_value = []
            assert newspaper.has_logo == False
            result = newspaper.set_logo_from_favicon()
            assert result == False
            assert newspaper.has_logo == False
