from django.apps import AppConfig


class ArchivedNewsConfig(AppConfig):
    name = 'xram_memory.archived_news'

    def ready(self):
        from xram_memory.archived_news import signals
