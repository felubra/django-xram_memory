from xram_memory.lib.news_fetcher.plugins.defaults import DefaultPDFCapture
from xram_memory.lib.news_fetcher.plugins.base import BasicInfoPluginBase
from xram_memory.lib.news_fetcher.plugins import pdf_captures
from xram_memory.lib.news_fetcher.plugins.parsers import (
    Goose3NewspaperArticleParser, NewspaperArticleParser)
from xram_memory.lib.news_fetcher.plugins import archives
import pdfkit
import pytest

G1_NEWS = 'https://g1.globo.com/politica/noticia/2019/05/23/apos-acordo-camara-derruba-emenda-que-limitava-poderes-de-auditores-fiscais.ghtml'
FOLHA_NEWS_URL = 'https://www1.folha.uol.com.br/poder/2019/05/votacao-que-aplicou-derrota-a-moro-abre-crise-no-centrao.shtml'


def test_pdf_plugin_default(datadir,  mocker):
    contents = (datadir / 'pagina-g1.html').read_text()
    mocker.patch("pdfkit.from_url")
    with DefaultPDFCapture.get_pdf_capture(FOLHA_NEWS_URL) as pdf_file:
        pdfkit.from_url.assert_called_once()


def test_g1_pdf_plugin(datadir,  mocker):
    contents = (datadir / 'pagina-g1.html').read_text()
    mocker.patch("pdfkit.from_string")
    with pdf_captures.G1PDFCapture.get_pdf_capture(FOLHA_NEWS_URL) as pdf_file:
        pdfkit.from_string.assert_called_once()


def test_parsers_result_is_valid_dictionary(datadir, mocker):
    contents = (datadir / 'pagina-g1.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        result = Parser.parse(url=G1_NEWS, html=contents)
        for key in BasicInfoPluginBase.BASIC_EMPTY_INFO.keys():
            assert key in result.keys()


def test_parsers_clean_is_called(datadir, mocker):
    contents = (datadir / 'pagina-g1.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        mocker.patch.object(BasicInfoPluginBase, 'clean')
        result = Parser.parse(url=G1_NEWS, html=contents)
        BasicInfoPluginBase.clean.assert_called_once()


def test_parsers_with_error(datadir, mocker):
    contents = (datadir / 'pagina-g1.html').read_text()
    for Parser in (Goose3NewspaperArticleParser, NewspaperArticleParser,):
        mocker.patch.object(BasicInfoPluginBase, 'clean', side_effect=OSError)
        with pytest.raises(ValueError):
            Parser.parse(url=G1_NEWS, html=contents)
