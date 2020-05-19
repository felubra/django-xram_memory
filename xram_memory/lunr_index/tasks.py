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

BACKEND = settings.LUNR_INDEX_BACKEND
FILE_PATH = settings.LUNR_INDEX_FILE_PATH
REBUILD_INTERVAL = settings.LUNR_INDEX_REBUILD_INTERVAL
REBUILD_TIMEOUT = settings.LUNR_INDEX_REBUILD_TIMEOUT
REMOTE_HOST = settings.LUNR_INDEX_REMOTE_HOST
REMOTE_SECRET = settings.LUNR_INDEX_REMOTE_SECRET
SAVE_DOCUMENT = settings.LUNR_INDEX_SAVE_DOCUMENT
SEARCH_FIELDS = settings.LUNR_INDEX_SEARCH_FIELDS

@shared_task(soft_time_limit=REBUILD_TIMEOUT)
def lunr_index_rebuild(self, lock_info=None):
    # Construa um índice com documentos e notícias
    # TODO: tentar novamente em caso de erro
    try:
        logger.debug("lunr_index_rebuild: início da execução")
        if BACKEND == LunrBackendValue.BACKEND_REMOTE:
            build_with_remote_elastic_lunr(REMOTE_HOST, REMOTE_SECRET, SEARCH_FIELDS, SAVE_DOCUMENT)
        else:
            build_with_lunr_py(FILE_PATH)
    finally:
        if lock_info:
            logger.debug("lunr_index_rebuild: limpando o lock")
            logger.debug(lock_info)
            release_memcache_lock(*lock_info)
