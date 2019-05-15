import os
import requests
import tempfile
from .plugins import *
from goose3 import Goose
from bs4 import BeautifulSoup
from newspaper import Article
from celery.contrib import rdb
from goose3.image import Image
from functools import lru_cache
import newspaper as newspaper3k
from django.conf import settings
from contextlib import contextmanager
from django.utils.functional import partition
from xram_memory.lib.stopwords import stopwords
from django.utils.timezone import make_aware, now
from django.utils.dateparse import parse_datetime
from .base_plugin import (ArchiveNewsFetcherPlugin, PDFCaptureNewsFetcherPlugin,
                          BasicInfoNewsFetcherPlugin)


class NewsFetcher:
    """
    Classe que concentra métodos para a busca de informações sobre notícias na web.
    """
    @staticmethod
    def fetch_archived_url(url):
        archived_url = ''
        for Plugin in ArchiveNewsFetcherPlugin.get_plugins():
            if Plugin.fetch(url):
                archived_url = Plugin.fetch(url)
        return archived_url

    @staticmethod
    def get_pdf_capture(url):
        specialized_plugins, failback_plugins = partition(
            lambda p: getattr(p, 'failback', False) == True,
            PDFCaptureNewsFetcherPlugin.get_plugins())
        for Plugin in specialized_plugins:
            if Plugin.matches(url):
                return Plugin.get_pdf_capture(url)
        else:
            try:
                return failback_plugins[0].get_pdf_capture(url)
            except IndexError:
                raise IndexError(
                    "Nenhum plugin de captura em pdf localizado.")

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
        """
        Dada uma URL, extraia informações básicas sobre uma notícia usando as bibliotecas
        newspaper3k e goose
        """
        # Tente extrair primeiro usando o newspaper3k e reutilize seu html, se possível
        newspaper_article = NewsFetcher._extract_using_newspaper(url)
        if newspaper_article:
            goose_article = NewsFetcher._extract_using_goose3(
                url, fetch_images=fetch_images, raw_html=newspaper_article.html)
        else:
            goose_article = NewsFetcher._extract_using_goose3(
                url, fetch_images=fetch_images)
        # ao menos um dos objetos deve estar preenchido
        if newspaper_article is None and goose_article is None:
            raise(ValueError(
                'Não foi possível extrair informações básicas sobre a notícia, pois nenhum dos extratores funcionou.'))
        # junte os objetos para tentar aproveitar de cada um alguma informação
        basic_info = NewsFetcher._merge_extractions(
            newspaper_article, goose_article)
        del newspaper_article
        del goose_article
        return basic_info

    @staticmethod
    def _merge_extractions(newspaper_article, goose_article):
        """
        Com base nas extrações passadas, constrói um dicionário em que a informação de cada uma é
        aproveitada, se existir, com prioridade para a extração da biblioteca newspaper.
        """
        def join_with_comma(list):
            return ",".join(list)

        try:
            # TODO: melhorar esse código, que está safo, mas não pythônico
            news_dict = {
                'title': newspaper_article.title if getattr(newspaper_article, 'title', None) else getattr(goose_article, 'title', None),
                'image': newspaper_article.top_image if getattr(newspaper_article, 'top_image', None) else goose_article.top_image.src if isinstance(getattr(goose_article, 'top_image', None), Image) else None,
                'body': newspaper_article.text if getattr(newspaper_article, 'text', None) else getattr(goose_article, 'cleaned_text', None),
                'teaser': getattr(newspaper_article, 'summary', None),
                # TODO: transformar a data de publicação para um objeto com ciência do
                # fuso-horário usado pelo Django
                'published_date': newspaper_article.publish_date if getattr(newspaper_article, 'publish_date', None) else getattr(goose_article, 'publish_date', None),
                'authors': join_with_comma(newspaper_article.authors if getattr(newspaper_article, 'authors', []) else getattr(goose_article, 'authors', [])),
                'keywords': getattr(newspaper_article, 'keywords', getattr(goose_article, 'tags', [])),
                'language': getattr(newspaper_article, 'meta_lang', getattr(goose_article, 'meta_lang', [])),
            }
            keywords_for_language = stopwords.get(news_dict["language"], [])
            if len(keywords_for_language) > 0:
                news_dict["keywords"] = [
                    keyword for keyword in news_dict["keywords"] if keyword not in stopwords[news_dict["language"]]
                ]
            # Se a data de publicação veio como string, tente transformá-la num objeto datetime
            if isinstance(news_dict['published_date'], str):
                try:
                    news_dict['published_date'] = parse_datetime(
                        news_dict['published_date'])
                except ValueError:
                    news_dict['published_date'] = None
            # Se a data de publicação não tem informações de fuso-horário, transforme-a para o fuso local
            if (news_dict['published_date'] and not news_dict['published_date'].tzinfo):
                news_dict['published_date'] = make_aware(
                    news_dict['published_date'], timezone=None, is_dst=False)
            return news_dict
        except Exception as err:
            raise(
                ValueError(
                    "Falha ao construir o dicionário com as informações básicas da notícia: {}."
                    .format(str(err))
                )
            )

    @staticmethod
    def _extract_using_newspaper(url, raw_html=None):
        """
        Tenta extrair usando a biblioteca newspaper3k
        """
        try:
            newspaper_article = Article(url)

            if raw_html:
                newspaper_article.download(input_html=raw_html)
            else:
                newspaper_article.download()
            newspaper_article.parse()
            newspaper_article.nlp()

            return newspaper_article
        except:
            return None
        finally:
            del raw_html

    @staticmethod
    def _extract_using_goose3(url, fetch_images=True, raw_html=None):
        """
        Tenta extrair usando a biblioteca goose3
        """
        try:
            goose = Goose({'enable_image_fetching': fetch_images})

            if raw_html:
                goose_article = goose.extract(raw_html=raw_html)
            else:
                goose_article = goose.extract(url=url)

            return goose_article
        except:
            return None
        finally:
            del raw_html

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_web_title(url):
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
        newspaper = newspaper3k.build(url)
        newspaper.download()
        newspaper.parse()
        # TODO: retornar o objeto apropriado para o modelo, não o 'lowlevel' da biblioteca
        # TODO: determinar o título com base no documento html
        return newspaper
