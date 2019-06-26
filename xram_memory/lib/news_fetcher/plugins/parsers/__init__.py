from django.utils.timezone import make_aware
from newspaper import Article
from xram_memory.lib.news_fetcher.plugins.base import BasicInfoPluginBase
from goose3 import Goose, Image


class NewspaperArticleParser(BasicInfoPluginBase):
    @classmethod
    def parse(cls, url, html=None):
        try:
            newspaper_article = Article(url)

            if html:
                newspaper_article.download(input_html=html)
            else:
                newspaper_article.download()
            newspaper_article.parse()
            newspaper_article.nlp()

            result = cls.clean({
                'title': getattr(newspaper_article, 'title', ''),
                'image': getattr(newspaper_article, 'top_image', ''),
                'body': getattr(newspaper_article, 'text', ''),
                'teaser': getattr(newspaper_article, 'summary', ''),
                'published_date': getattr(newspaper_article, 'publish_date', None),
                'language': getattr(newspaper_article, 'meta_lang', ''),
                'authors': ",".join(getattr(newspaper_article, 'authors', [])),
                'keywords': cls.extract_taxonomy(getattr(newspaper_article, 'keywords', []), cls.KEYWORDS_REGEX),
                'subjects': cls.extract_taxonomy(getattr(newspaper_article, 'keywords', []), cls.SUBJECTS_REGEX),
            })
            del newspaper_article
            return result
        except Exception as err:
            raise(
                ValueError(
                    "Falha ao construir o dicionário com as informações básicas da notícia: {}."
                    .format(str(err))
                )
            )
        finally:
            if html:
                del html


class Goose3NewspaperArticleParser(BasicInfoPluginBase):
    @classmethod
    def parse(cls, url, html=None):
        """
        Tenta extrair usando a biblioteca goose3
        """
        try:
            goose = Goose({'enable_image_fetching': True})

            if html:
                goose_article = goose.extract(raw_html=html)
            else:
                goose_article = goose.extract(url=url)
            meta_keywords = [keyword.strip() for keyword in getattr(
                goose_article, 'meta_keywords', '').split(',')]
            keywords = list(
                set(getattr(goose_article, 'keywords', []) + meta_keywords))
            result = cls.clean({
                'title': getattr(goose_article, 'title', ''),
                'image': (goose_article.top_image.src
                          if isinstance(getattr(goose_article, 'top_image', None), Image) else ''),
                'body': getattr(goose_article, 'cleaned_text', ''),
                'teaser': getattr(goose_article, 'meta_description'),
                'published_date': getattr(goose_article, 'publish_date', ''),
                'authors': ",".join(getattr(goose_article, 'authors', [])),
                'language': getattr(goose_article, 'meta_lang', ''),
                'keywords': cls.extract_taxonomy(keywords, cls.KEYWORDS_REGEX),
                'subjects': cls.extract_taxonomy(keywords, cls.SUBJECTS_REGEX),
            })
            del goose_article
            return result
        except Exception as err:
            raise(
                ValueError(
                    "Falha ao construir o dicionário com as informações básicas da notícia: {}."
                    .format(str(err))
                )
            )
        finally:
            if html:
                del html
