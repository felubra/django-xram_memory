from xram_memory.lunr_index.util import LunrBackendValue
from xram_memory.utils import release_memcache_lock
from django.conf import settings
from celery import shared_task
from loguru import logger
import requests

from xram_memory.lunr_index.lib.index_builders import (
    build_with_lunr_py,
    build_with_remote_elastic_lunr
)

@shared_task(soft_time_limit=settings.LUNR_INDEX_REBUILD_TIMEOUT)
def lunr_index_rebuild(self, lock_info=None, sync=False):
    # Construa um índice com documentos e notícias
    try:
        logger.debug("lunr_index_rebuild: início da execução")
        if settings.LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_REMOTE:
            build_with_remote_elastic_lunr(
                settings.LUNR_INDEX_REMOTE_HOST,
                settings.LUNR_INDEX_REMOTE_SECRET,
                settings.LUNR_INDEX_SEARCH_FIELDS,
                settings.LUNR_INDEX_SAVE_DOCUMENT,
                retry=not sync
            )
        elif settings.LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_LOCAL:
            build_with_lunr_py(settings.LUNR_INDEX_FILE_PATH)
    finally:
        if lock_info:
            logger.debug("lunr_index_rebuild: limpando o lock")
            logger.debug(lock_info)
            release_memcache_lock(*lock_info)
