from django.apps import AppConfig


class LunrSearchConfig(AppConfig):
    name = 'xram_memory.lunr_search'

    def ready(self):
        from xram_memory.lunr_search import signals
