from django.db.models.signals import post_save, post_delete, m2m_changed
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.utils import celery_is_avaliable, memcache_lock
from xram_memory.utils.decorators import disable_for_loaddata
from xram_memory.utils.classes import SignalProcessor
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.logger.decorators import log_process
from datetime import datetime, timedelta
from .tasks import lunr_index_rebuild
from loguru import logger


class LunrIndexSignalProcessor(SignalProcessor):
    """Observa os modelos registrados através de seus sinais e agenda o trabalho de indexação.
    Pode ser desligado via runtime.
    """

    def __init__(self, rebuild_interval, rebuild_timeout):
        self.rebuild_interval = rebuild_interval
        self.rebuild_timeout = rebuild_timeout
        self.models = [News, Newspaper, Keyword, Subject, Document]
        self.signals = [post_save, post_delete, m2m_changed]
        super().__init__()

    @log_process(operation="agendar para reconstruir índice lunr")
    @disable_for_loaddata
    def handler(self, *arsg, **kwargs):
        """
        Com base nas configurações, obtém uma trava e agenda a execução das funções de indexação
        """
        sync = not celery_is_avaliable()
        with memcache_lock(
            "LUNR_INDEX_REBUILD",
            "SIGNAL_SENDER",
            self.rebuild_interval + self.rebuild_timeout,
            sync,
        ) as (
            acquired,
            lock_info,
        ):
            if acquired:
                logger.debug("schedule_lunr_index_rebuild: lock adquirido")
                if not sync:
                    lunr_index_rebuild.apply_async(
                        eta=datetime.utcnow()
                        + timedelta(seconds=self.rebuild_interval),
                        args=[lock_info, sync],
                    )
                else:
                    lunr_index_rebuild.apply(args=[lock_info, sync])
            else:
                logger.debug("schedule_lunr_index_rebuild: lock NÃO adquirido")
