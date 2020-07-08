from django.db.models.signals import post_save, post_delete, m2m_changed
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.utils import celery_is_avaliable, memcache_lock
from xram_memory.utils.decorators import disable_for_loaddata
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.logger.decorators import log_process
from datetime import datetime, timedelta
from .tasks import lunr_index_rebuild
from loguru import logger



class SignalProcessor:
    """ Observa os modelos registrados através de seus sinais e agenda o trabalho de indexação.
    Pode ser desligado via runtime.
    """
    def __init__(self, rebuild_interval, rebuild_timeout):
        self.rebuild_interval = rebuild_interval
        self.rebuild_timeout = rebuild_timeout
        #TODO: permitir configuração
        self.models = [News, Newspaper, Keyword, Subject, Document]
        self.setup()

    def setup(self):
        """
        Para cada modelo, conecta o agendamento do trabalho ao sinal suportado.
        """
        for model in self.models:
            post_save.connect(self.schedule_lunr_index_rebuild, model)
            m2m_changed.connect(self.schedule_lunr_index_rebuild, model)
            post_delete.connect(self.schedule_lunr_index_rebuild, model)

    def teardown(self):
        """
        Desconecta os sinais outrora conectados.
        """
        for model in self.models:
            post_save.disconnect(self.schedule_lunr_index_rebuild, model)
            m2m_changed.disconnect(self.schedule_lunr_index_rebuild, model)
            post_delete.disconnect(self.schedule_lunr_index_rebuild, model)

    @log_process(operation="agendar para reconstruir índice lunr")
    @disable_for_loaddata
    def schedule_lunr_index_rebuild(self, **kwargs):
        """
        Com base nas configurações, obtém uma trava e agenda a execução das funções de indexação
        """
        sync = not celery_is_avaliable()
        with memcache_lock(
                'LUNR_INDEX_REBUILD', 'SIGNAL_SENDER',
                self.rebuild_interval + self.rebuild_timeout, sync
            ) as (acquired, lock_info,):
            if acquired:
                logger.debug("schedule_lunr_index_rebuild: lock adquirido")
                if not sync:
                    lunr_index_rebuild.apply_async(
                        eta=datetime.utcnow() + timedelta(seconds=self.rebuild_interval),
                        args=[lock_info, sync]
                    )
                else:
                    lunr_index_rebuild.apply(args=[lock_info, sync])










