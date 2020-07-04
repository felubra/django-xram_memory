import factory
from django.db.models.signals import post_delete, post_save, pre_delete, m2m_changed
from contextlib import contextmanager
from .. import fixtures
from xram_memory.artifact.models import News
from unittest.mock import patch
from loguru import logger
logger.remove()
from xram_memory.lib import NewsFetcher


@contextmanager
def basic_news():
    with factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete):
        news = fixtures.NewsFactory()
        news.save()
    yield news

@contextmanager
def basic_news_with_newspaper():
    with factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete):
        newspaper = fixtures.NewspaperFactory()
        newspaper.save()
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html",
            newspaper=newspaper
        )
        with patch.object(NewsFetcher, 'fetch_basic_info', return_value=fixtures.NEWS_INFO_MOCK):
            news.set_basic_info()
        news.save()
    yield news
