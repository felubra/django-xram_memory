import os
import copy
import tempfile
import requests
from .plugins import *
from bs4 import BeautifulSoup
from functools import lru_cache
import newspaper as newspaper3k
from contextlib import contextmanager
from django.utils.functional import partition
from django.core.validators import URLValidator
from .plugins.base import ArchivePluginBase, PDFCapturePluginBase, BasicInfoPluginBase


url_validator = URLValidator()


class NewsFetcher:
    """
    Classe que concentra métodos para a busca de informações sobre notícias na web.
    """
    @staticmethod
    def fetch_archived_url(url):
        plugins = ArchivePluginBase.get_plugins()
        failures = []
        try:
            url_validator(url)
            if not len(plugins):
                raise RuntimeError(
                    "Nenhum plugin para busca de versões arquivadas registrado.")
            for Plugin in plugins:
                try:
                    archived_url = Plugin.fetch(url)
                    if archived_url:
                        return archived_url
                except Exception as e:
                    failures.append(e)
        except:
            raise
        else:
            # Não obtivemos um retorno satisfatório dos plugins e alguns podem até ter falhado,
            # vamos relançar as exceções dos que falharam.
            if len(failures):
                raise RuntimeError(
                    "Falha na captura de uma versão arquivada - alguns plugins falharam") from Exception(failures)
            # Todos os plugins rodaram com sucesso, mas nenhum obteve um resultado, retorne uma
            # string vazia.
            return ''

    @staticmethod
    def get_pdf_capture(url):
        plugins = PDFCapturePluginBase.get_plugins()
        failures = []
        try:
            url_validator(url)
            if not len(plugins):
                raise RuntimeError(
                    "Nenhum plugin para captura de páginas em pdf registrado.")
            for Plugin in plugins:
                try:
                    if Plugin.matches(url):
                        return Plugin.get_pdf_capture(url)
                except Exception as e:
                    failures.append(e)
        except:
            raise
        else:
            # Não obtivemos um retorno satisfatório dos plugins e alguns podem até ter falhado,
            # vamos relançar as exceções dos que falharam.
            if len(failures):
                raise RuntimeError(
                    "Falha na captura de uma versão arquivada - alguns plugins falharam") from Exception(failures)
            # Não existe a possibilidade de passarmos por todos os plugins sem erro, pois deve existir
            # ao menos um plugin que funcione sobre todas as urls e, portanto, tenha falhado.

    @staticmethod
    @contextmanager
    def fetch_image(image_url):
        """
        Captura uma imagem de uma notícia e, como gerenciador de contexto, retorna um ponteiro para
        o arquivo criado. Fecha e apaga o arquivo ao final.
        """
        url_validator(image_url)
        fd, file_path, = tempfile.mkstemp()
        response = requests.get(image_url, allow_redirects=True)
        response.raise_for_status()
        with open(fd, 'rb+') as f:
            f.write(response.content)
            yield f
        os.remove(file_path)

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_basic_info(url, fetch_images=True):
        plugins = BasicInfoPluginBase.get_plugins()
        failures = []
        basic_info = copy.deepcopy(BasicInfoPluginBase.BASIC_EMPTY_INFO)
        try:
            url_validator(url)
            if not len(plugins):
                raise RuntimeError(
                    "Nenhum plugin para busca de informações básicas registrado.")
            with requests.get(url, allow_redirects=True) as r:
                r.raise_for_status()
                html = r.content
                for plugin in plugins:
                    try:
                        result = plugin.parse(url, html=html)
                        """
                        Utilize uma abordagem conservadora em que um valor no dicionário de dados
                        da notícia só é alterado se estiver vazio. A exceção fica para o caso das
                        palavras-chave (quanto mais palavras melhor).
                        """
                        for key in BasicInfoPluginBase.BASIC_EMPTY_INFO.keys():
                            if key == 'keywords':
                                for keyword in result['keywords']:
                                    if keyword not in basic_info['keywords']:
                                        basic_info['keywords'].append(
                                            keyword)
                                continue
                            if result[key] not in ('', [], None,):
                                if basic_info[key] in ('', [], None,):
                                    basic_info[key] = result[key]
                    except Exception as e:
                        failures.append(e)
                if basic_info != BasicInfoPluginBase.BASIC_EMPTY_INFO:
                    return basic_info
        except:
            raise
        else:
            # Não obtivemos um retorno satisfatório dos plugins e alguns podem até ter falhado,
            # vamos relançar as exceções dos que falharam.
            if len(failures):
                raise RuntimeError(
                    "Falha na obtenção de informações sobre a notícia - alguns plugins falharam") from Exception(failures)
            else:
                # No raro caso de todos plugins não terem falhado, mas mesmo assim não tiverem obtido
                # informações, lance uma exceção, pois é esperado dessa função o retorno de um dicionário
                # com as informações da notícia.
                raise RuntimeError(
                    "Falha na obtenção de informações sobre a notícia - nenhum plugin obteve informações básicas sobre a notícia.")

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_web_title(url):
        # TODO: usar uma biblioteca para buscar o título corretamente
        url_validator(url)
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, features="lxml")
            return soup.title.text
        except AttributeError:
            return url

    @staticmethod
    @lru_cache(maxsize=2)
    def build_newspaper(url):
        url_validator(url)
        # TODO: usar uma biblioteca para buscar o título corretamente
        newspaper = newspaper3k.build(url)
        newspaper.download()
        newspaper.parse()
        # TODO: retornar o objeto apropriado para o modelo, não o 'lowlevel' da biblioteca
        # TODO: determinar o título com base no documento html
        return newspaper
