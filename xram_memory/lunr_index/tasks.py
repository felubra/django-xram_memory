from xram_memory.lunr_index.util import LunrBackendValue
from xram_memory.utils import release_memcache_lock
from django.conf import settings
from celery import shared_task
from loguru import logger
import requests

from xram_memory.lunr_index.lib.index_builders import (
    LunrIndexBuilder,
    RemoteElasticLunrIndexBuilder
)

@shared_task(soft_time_limit=settings.LUNR_INDEX_REBUILD_TIMEOUT)
def lunr_index_rebuild(lock_info=None, sync=False):
    # Construa um índice com documentos e notícias
    try:
        logger.debug("lunr_index_rebuild: início da execução")
        if settings.LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_REMOTE:
            RemoteElasticLunrIndexBuilder.build(
                settings.LUNR_INDEX_REMOTE_HOST,
                settings.LUNR_INDEX_REMOTE_SECRET,
                settings.LUNR_INDEX_SEARCH_FIELDS,
                settings.LUNR_INDEX_SAVE_DOCUMENT,
                retry=False
            )
        elif settings.LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_LOCAL:
            LunrIndexBuilder.build(settings.LUNR_INDEX_FILE_PATH)
    finally:
        if lock_info:
            logger.debug("lunr_index_rebuild: limpando o lock")
            logger.debug(lock_info)
            release_memcache_lock(*lock_info)
