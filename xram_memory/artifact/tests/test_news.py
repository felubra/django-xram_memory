import pytest
from unittest import mock as mocker

from xram_memory.artifact.models.news import News


@pytest.fixture
def news_valid_initial():
    return News(url='https://web.archive.org/web/20180402192047/https://www.gazetadopovo.com.br/educacao/pesquisa-do-mit-universidade-publica-gratuita-pode-prejudicar-alunos-de-baixa-renda-4dvkdiewbpxj24hl6lber8vhe/')


@pytest.fixture
def news_invalid_no_url():
    return News()


def test_initial_state(news_valid_initial):
    assert news_valid_initial.has_basic_info == False
    assert news_valid_initial.has_pdf_capture == False
    assert news_valid_initial.has_image == False
    assert news_valid_initial.image_capture_indexing is None
    assert news_valid_initial.thumbnail is None
    assert news_valid_initial.published_year is None


@pytest.mark.django_db
def test_save_calls_set_web_title(news_valid_initial):
    with mocker.patch("xram_memory.artifact.models.news.News.set_web_title") as set_web_title_mocked:
        with pytest.raises(ValueError) as excinfo:
            news_valid_initial.save()
        assert "Não é possível criar um artefato sem título." in str(
            excinfo.value)
        set_web_title_mocked.assert_called()


def test_raises_for_no_url(news_invalid_no_url):
    with pytest.raises(ValueError) as excinfo:
        news_invalid_no_url.save()
    assert "Você precisa definir um endereço para a notícia." in str(
        excinfo.value)
