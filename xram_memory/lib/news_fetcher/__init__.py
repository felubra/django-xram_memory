import os
import tempfile
import requests
from .plugins import *
from bs4 import BeautifulSoup
from functools import lru_cache
import newspaper as newspaper3k
from contextlib import contextmanager
from django.utils.functional import partition
from .plugin import (ArchiveNewsFetcherPlugin, PDFCaptureNewsFetcherPlugin,
                     BasicInfoNewsFetcherPlugin)


class NewsFetcher:
    """
    Classe que concentra métodos para a busca de informações sobre notícias na web.
    """
    @staticmethod
    def fetch_archived_url(url):
        archived_url = ''
        plugins = ArchiveNewsFetcherPlugin.get_plugins()
        failed_plugins_count = 0
        try:
            for Plugin in ArchiveNewsFetcherPlugin.get_plugins():
                try:
                    archived_url = Plugin.fetch(url)
                    if archived_url:
                        return archived_url
                except:
                    failed_plugins_count += 1
                    pass
        except:
            raise
        else:
            if failed_plugins_count == len(plugins):
                raise RuntimeError(
                    "Nenhum plugin de arquivo funcionou.")

    @staticmethod
    def get_pdf_capture(url):
        failed_plugins_count = 0
        specialized_plugins, failback_plugins = partition(
            lambda p: getattr(p, 'failback', False) == True,
            PDFCaptureNewsFetcherPlugin.get_plugins())
        try:
            for Plugin in specialized_plugins:
                try:
                    if Plugin.matches(url):
                        return Plugin.get_pdf_capture(url)
                except:
                    failed_plugins_count += 1
                    pass
            else:
                try:
                    return failback_plugins[0].get_pdf_capture(url)
                except IndexError:
                    raise RuntimeError(
                        "Nenhum plugin de captura em pdf registrado.")
                except:
                    raise RuntimeError(
                        "Nenhum plugin de captura em pdf funcionou.")
        except:
            raise
        else:
            if failed_plugins_count == len(specialized_plugins):
                raise RuntimeError(
                    "Nenhum plugin de captura em pdf funcionou.")

    @staticmethod
    @contextmanager
    def fetch_image(image_url):
        """
        Captura uma imagem de uma notícia e, como gerenciador de contexto, retorna um ponteiro para
        o arquivo criado. Fecha e apaga o arquivo ao final.
        """
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
        failed_plugins_count = 0
        plugins = BasicInfoNewsFetcherPlugin.get_plugins()
        basic_info = BasicInfoNewsFetcherPlugin.BASIC_EMPTY_INFO
        try:
            if len(plugins):
                with requests.get(url, allow_redirects=True) as r:
                    r.raise_for_status()
                    html = r.content.decode("utf-8")
                    for plugin in plugins:
                        try:
                            result = plugin.parse(url, html=html)
                            """
                            Utilize uma abordagem conservadora em que um valor no dicionário de dados
                            da notícia só é alterado se estiver vazio. A exceção fica para o caso das
                            palavras-chave (quanto mais palavras melhor).
                            """
                            for key in BasicInfoNewsFetcherPlugin.BASIC_EMPTY_INFO.keys():
                                if key == 'keywords':
                                    for keyword in result['keywords']:
                                        if keyword not in basic_info['keywords']:
                                            basic_info['keywords'].append(
                                                keyword)
                                    continue
                                basic_info[key] = (result[key] if result[key] not in ('', [], None,) and (getattr(
                                    basic_info, key, None) is None or basic_info[key] in ('', [],)) else basic_info[key])
                        except:
                            # não falhe completamente se apenas um plugin falhar, mas mantenha um
                            # registro da quantidade de plugins que falharam...
                            failed_plugins_count += 1
                            pass
            else:
                raise RuntimeError(
                    "Nenhum plugin para busca de informações básicas registrado.")
        except:
            raise
        else:
            # ...se todos os plugins falharam, então falhe.
            if failed_plugins_count == len(plugins):
                raise RuntimeError(
                    "Todos os plugins de captura de dados básicos falharam.")
            return basic_info

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_web_title(url):
        # TODO: usar uma biblioteca para buscar o título corretamente
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
        # TODO: usar uma biblioteca para buscar o título corretamente
        newspaper = newspaper3k.build(url)
        newspaper.download()
        newspaper.parse()
        # TODO: retornar o objeto apropriado para o modelo, não o 'lowlevel' da biblioteca
        # TODO: determinar o título com base no documento html
        return newspaper
