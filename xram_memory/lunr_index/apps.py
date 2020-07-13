from django.apps import AppConfig
from .util import LunrBackendValue

class LunrIndexConfig(AppConfig):
    name = 'xram_memory.lunr_index'

    def ready(self):
        # importe aqui, pois precisamos esperar as outras aplicações iniciar
        from .signals import LunrIndexSignalProcessor
        from django.conf import settings
        # Somente conecte os sinais se o backend for válido
        if getattr(settings, 'LUNR_INDEX_BACKEND', None) in LunrBackendValue.VALID_BACKENDS:
            REBUILD_INTERVAL = settings.LUNR_INDEX_REBUILD_INTERVAL
            REBUILD_TIMEOUT = settings.LUNR_INDEX_REBUILD_TIMEOUT
            self.signal_processor = LunrIndexSignalProcessor(REBUILD_INTERVAL, REBUILD_TIMEOUT)
