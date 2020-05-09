from django.apps import AppConfig


class LunrIndexConfig(AppConfig):
    name = 'xram_memory.lunr_index'

    def ready(self):
        from xram_memory.lunr_index import signals
