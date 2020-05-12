from django.db.models.signals import post_save, post_delete, m2m_changed
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.utils import celery_is_avaliable, memcache_lock
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.logger.decorators import log_process
from datetime import datetime, timedelta
from .tasks import lunr_index_rebuild
from django.conf import settings
from loguru import logger

SETTINGS = settings.LUNR_INDEX
REBUILD_INTERVAL = SETTINGS['REBUILD_INTERVAL']
REBUILD_TIMEOUT = SETTINGS['REBUILD_TIMEOUT']

@log_process(operation="agendar para reconstruir índice lunr")
def schedule_lunr_index_rebuild(sender, instance, **kwargs):
    sync = not celery_is_avaliable()
    with memcache_lock('LUNR_INDEX_REBUILD', 'SIGNAL_SENDER', REBUILD_INTERVAL + REBUILD_TIMEOUT, sync) as (acquired, lock_info,):
        if acquired:
            logger.debug("schedule_lunr_index_rebuild: lock adquirido")
            if not sync:
                lunr_index_rebuild.apply_async(eta=datetime.utcnow() + timedelta(seconds=REBUILD_INTERVAL), args=[lock_info])
            else:
                lunr_index_rebuild.apply(args=[lock_info])
    # FIXME: implementar failback para o caso do celery não estar disponível


for Model in [News, Newspaper, Keyword, Subject, Document]:
    post_save.connect(schedule_lunr_index_rebuild, Model)
    m2m_changed.connect(schedule_lunr_index_rebuild, Model)
    post_delete.connect(schedule_lunr_index_rebuild, Model)
