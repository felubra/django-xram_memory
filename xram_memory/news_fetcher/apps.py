from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class NewsFetcherConfig(AppConfig):
    name = 'xram_memory.news_fetcher'

    def ready(self):
        from xram_memory.news_fetcher import receivers
