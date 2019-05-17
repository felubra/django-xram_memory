from django.utils.timezone import make_aware, now
from contextlib import contextmanager
from bs4 import BeautifulSoup
import requests
import tempfile
import pdfkit
import os
import re


class DefaultPDFCapture():
    """
    Um plugin padrão para captura de notícias em PDF.
    """
    @staticmethod
    def matches(url):
        return True

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
