from xram_memory.lib.news_fetcher.base_plugin import PDFCaptureNewsFetcherPlugin
from django.utils.timezone import make_aware, now
from contextlib import contextmanager
from bs4 import BeautifulSoup
import requests
import tempfile
import pdfkit
import os
import re


class DefaultPDFCapture(PDFCaptureNewsFetcherPlugin):
    failback = True

    @staticmethod
    @contextmanager
    def get_pdf_capture(url):
        """
        Captura uma página em pdf e, como gerenciador de contexto, retorna um ponteiro para o
        arquivo temporário criado. Fecha e apaga o arquivo temporário ao final.
        """
        fd, file_path, = tempfile.mkstemp()
        pdfkit.from_url(url, file_path, options={
            'print-media-type': None,
            'disable-javascript': None,
            'footer-center': now(),
            'footer-font-size': 8,
            'header-center': url,
            'header-font-size': 6,
            'log-level': 'none',
            'image-quality': 85})
        with open(fd, 'rb') as f:
            yield f
        os.remove(file_path)


class G1PDFCapture(PDFCaptureNewsFetcherPlugin):
    """
    Classe que implementa a captura de notícias do portal G1 da Globo (https://g1.globo.com/).
    O site desfoca as imagens com estilos e um atributo src contendo dados (codificados em Base 64)
    para uma imagem com apenas um borrão da imagem em tamanho original. O link para a imagem em
    tamanho original fica no atributo "data-max-size-url" de um elemento div que envolve essas
    imagens, conforme abaixo:

    <div class="progressive-img" data-max-size-url="https://s2.glbimg.com/...">
        <img class="progressive-draft" src="data:image/jpeg;base64,...">
    </div>

    O propósito desse plugin, que somente funciona com páginas do G1, é substituir o atributo `src`
    dessas imagens pelo link em alta resolução da imagem para, somente então, fazer a captura da
    página. A função get_pdf_capture faz isso, mas também faz a captura normal se não encontrar os
    elementos sobre os quais fazer a substituição.
    """
    @staticmethod
    def matches(url):
        return bool(re.match(r"^https?:\/\/g1\.globo\.com\/.*$", url))

    @staticmethod
    @contextmanager
    def get_pdf_capture(url):
        """
        Faz o mesmo que `DefaultPDFCapture.get_pdf_capture`, mas também faz o processamento descrito
        na documentação da classe antes de entregar o arquivo com a captura num gerenciador de
        contexto.
        """
        with requests.get(url, allow_redirects=True) as r:
            r.raise_for_status()
            html = r.content.decode('utf-8')
            try:
                soup = BeautifulSoup(html, features="lxml")
                wrappers = soup.find_all("div", ["progressive-img"])
                for wrapper in wrappers:
                    image = wrapper.find("img", "progressive-draft")
                    if image:
                        image["src"] = wrapper["data-max-size-url"]
                        image["style"] = "filter: none;"
                html = str(soup)
            finally:
                fd, file_path, = tempfile.mkstemp()
                pdfkit.from_string(html, file_path, options={
                    'print-media-type': None,
                    'disable-javascript': None,
                    'footer-center': now(),
                    'footer-font-size': 8,
                    'header-center': url,
                    'header-font-size': 6,
                    'log-level': 'none',
                    'image-quality': 85})
                with open(fd, 'rb') as f:
                    yield f
                os.remove(file_path)
