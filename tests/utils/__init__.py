import factory
from django.db.models.signals import post_delete, post_save, pre_delete, m2m_changed
from contextlib import contextmanager
from .. import fixtures
from xram_memory.artifact.models import News
from unittest.mock import patch
from loguru import logger
from xram_memory.lib import NewsFetcher
from django.apps import apps

logger.remove()

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

def toggle_elastic_search_signals(disable=True):
    try:
        signal_processor = apps.get_app_config('django_elasticsearch_dsl').signal_processor
    except:
        return
    else:
        if disable:
            signal_processor.teardown()
        else:
            signal_processor.setup()

def toggle_local_search_signals(disable=True):
    try:
        signal_processor = apps.get_app_config('lunr_index').signal_processor
    except Exception as e:
        return
    else:
        if disable:
            signal_processor.teardown()
        else:
            signal_processor.setup()


def toggle_artifact_signals(disable=True, models=[]):
    if not models:
        return
    try:
        signal_processors = apps.get_app_config('artifact').signal_processors
    except Exception as e:
        return
    else:
        for model in models:
            signal_processor = signal_processors[model]
            if disable:
                signal_processor.teardown()
            else:
                signal_processor.setup()

def toggle_indexing_apps_signals(disable=True):
    toggle_elastic_search_signals(disable)
    toggle_local_search_signals(disable)

@contextmanager
def without_indexing_apps():
    toggle_indexing_apps_signals()
    try:
        yield
    finally:
        toggle_indexing_apps_signals(False)

@contextmanager
def without_local_search():
    toggle_local_search_signals()
    try:
        yield
    finally:
        toggle_local_search_signals(False)

@contextmanager
def without_elastic_search():
    toggle_elastic_search_signals()
    try:
        yield
    finally:
        toggle_elastic_search_signals(False)


@contextmanager
def without_elastic_search():
    toggle_elastic_search_signals()
    try:
        yield
    finally:
        toggle_elastic_search_signals(False)

@contextmanager
def without_artifact_auto_processing(models=["documents", "news", "newspaper"]):
    toggle_artifact_signals(True, models)
    try:
        yield
    finally:
        toggle_artifact_signals(False, models)

class DisabledIndexingAppsMixin(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        toggle_indexing_apps_signals()

    @classmethod
    def tearDownClass(cls):
        toggle_indexing_apps_signals(False)
        super().tearDownClass()

