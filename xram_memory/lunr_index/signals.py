from django.db.models.signals import post_save, post_delete, m2m_changed
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.utils import celery_is_avaliable, memcache_lock
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.logger.decorators import log_process
from datetime import datetime, timedelta
from .tasks import lunr_index_rebuild
from django.conf import settings
from loguru import logger
from xram_memory.lunr_index.util import LunrBackendValue


class SignalProcessor:
    def __init__(self, rebuild_interval, rebuild_timeout):
        self.rebuild_interval = rebuild_interval
        self.rebuild_timeout = rebuild_timeout
        #TODO: permitir configuração
        self.models = [News, Newspaper, Keyword, Subject, Document]
        self.setup()

    def setup(self):
        for model in self.models:
            post_save.connect(self.schedule_lunr_index_rebuild, model)
            m2m_changed.connect(self.schedule_lunr_index_rebuild, model)
            post_delete.connect(self.schedule_lunr_index_rebuild, model)

    def teardown(self):
        for model in self.models:
            post_save.disconnect(self.schedule_lunr_index_rebuild, model)
            m2m_changed.disconnect(self.schedule_lunr_index_rebuild, model)
            post_delete.disconnect(self.schedule_lunr_index_rebuild, model)

    @log_process(operation="agendar para reconstruir índice lunr")
    def schedule_lunr_index_rebuild(self, sender, instance, **kwargs):
        # FIXME: implementar failback para o caso do celery não estar disponível
        sync = not celery_is_avaliable()
        with memcache_lock('LUNR_INDEX_REBUILD', 'SIGNAL_SENDER', REBUILD_INTERVAL + REBUILD_TIMEOUT, sync) as (acquired, lock_info,):
            if acquired:
                logger.debug("schedule_lunr_index_rebuild: lock adquirido")
                if not sync:
                    lunr_index_rebuild.apply_async(eta=datetime.utcnow() + timedelta(seconds=REBUILD_INTERVAL), args=[lock_info])
                else:
                    lunr_index_rebuild.apply(args=[lock_info])










