from xram_memory.lib import NewsFetcher
from xram_memory.lib.news_fetcher.plugins.defaults import DefaultPDFCapture
from xram_memory.lib.news_fetcher.plugins.base import BasicInfoPluginBase
from xram_memory.lib.news_fetcher.plugins import pdf_captures
from xram_memory.lib.news_fetcher.plugins.parsers import (
    Goose3NewspaperArticleParser, NewspaperArticleParser)
from xram_memory.lib.news_fetcher.plugins import archives
import pdfkit
import pytest

G1_NEWS_URL = 'https://g1.globo.com/politica/noticia/2019/05/23/apos-acordo-camara-derruba-emenda-que-limitava-poderes-de-auditores-fiscais.ghtml'
FOLHA_NEWS_URL = 'https://www1.folha.uol.com.br/poder/2019/05/votacao-que-aplicou-derrota-a-moro-abre-crise-no-centrao.shtml'


"""
FIXME: usar o mecanismo de descoberta dos plugins ao invés de usá-los
de forma hardcoded aqui, pois novos plugins podem ser adicionados, nomes
mudados etc.
"""

def test_pdf_plugin_default(datadir,  mocker):
    """
    Verifica se o plugin de geração de visualizações pdf padrão invoca a
    função da biblioteca para geração de pdfs
    """
    contents = (datadir / 'pagina-folha.html').read_text()
    mocker.patch("pdfkit.from_url")
    with DefaultPDFCapture.get_pdf_capture(FOLHA_NEWS_URL) as pdf_file:
        pdfkit.from_url.assert_called_once()


def test_g1_pdf_plugin(datadir,  mocker):
    """
    Verifica se o plugin de geração de visualizações pdf do G1 invoca a
    função da biblioteca para geração de pdfs
    """
    contents = (datadir / 'pagina-g1.html').read_text()
    mocker.patch("pdfkit.from_string")
    with pdf_captures.G1PDFCapture.get_pdf_capture(G1_NEWS_URL) as pdf_file:
        pdfkit.from_string.assert_called_once()


def test_parsers_result_is_valid_dictionary(datadir, mocker):
    """
    Verifica se os plugins parsers de informação retornam todas as chaves
    definidas no dicionário BasicInfoPluginBase.BASIC_EMPTY_INFO, ou seja,
    todos os plugins devem retornar um objeto consistente
    """
    contents = (datadir / 'pagina-folha.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        result = Parser.parse(url=FOLHA_NEWS_URL, html=contents)
        for key in BasicInfoPluginBase.BASIC_EMPTY_INFO.keys():
            assert key in result.keys()


def test_parsers_clean_is_called(datadir, mocker):
    """
    Verifica se os plugins parsers de informação chamam a função clean()
    de BasicInfoPluginBase
    """
    contents = (datadir / 'pagina-folha.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        mocker.patch.object(BasicInfoPluginBase, 'clean')
        result = Parser.parse(url=FOLHA_NEWS_URL, html=contents)
        BasicInfoPluginBase.clean.assert_called_once()


def test_parsers_with_error(datadir, mocker):
    """
    Simula um erro no sistema e espera que o plugin invoque uma exceção
    ValueError quando chamada a função parse()
    """
    contents = (datadir / 'pagina-folha.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        mocker.patch.object(BasicInfoPluginBase, 'clean', side_effect=OSError)
        with pytest.raises(ValueError):
            Parser.parse(url=FOLHA_NEWS_URL, html=contents)
