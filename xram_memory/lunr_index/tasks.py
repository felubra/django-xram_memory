from xram_memory.utils import memcache_lock, release_memcache_lock
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from celery import shared_task, group
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from django.apps import apps
from loguru import logger
from lunr import lunr
import json


SETTINGS = settings.LUNR_INDEX
FILE_PATH = SETTINGS['FILE_PATH']
REBUILD_TIMEOUT = SETTINGS['REBUILD_TIMEOUT']
REBUILD_INTERVAL = SETTINGS['REBUILD_INTERVAL']

@shared_task(soft_time_limit=REBUILD_TIMEOUT)
def lunr_index_rebuild(self, lock_info=None):
    # Construa um índice com documentos e notícias
    # TODO: otimizar
    # TODO: tentar novamente em caso de erro
    logger.debug("lunr_index_rebuild: início da execução")
    News = apps.get_model('artifact', 'News')
    Documents = apps.get_model('artifact', 'Document')

    items = []
    items += [
        {
            'id': n.id,
            'title': n.title,
            'teaser': n.teaser,
            'subjects': " ".join([k.name for k in n.subjects.all()]),
            'keywords': " ".join([k.name for k in n.keywords.all()]),
        } for n in News.objects.prefetch_related('keywords', 'subjects')
    ]
    items += [
        {
            'id': d.id,
            'title': d.name,
            'teaser': d.description,
            'subjects': " ".join([k.name for k in d.subjects.all()]),
            'keywords': " ".join([k.name for k in d.keywords.all()]),
        } for d in Documents.objects.prefetch_related('keywords', 'subjects')
    ]
    try:
        if (len(items)):
            idx = lunr(
                ref='id',
                fields=[k for k in items[0].keys() if k != 'id'],
                documents=items, languages=['pt','en']
            )
            serialized = idx.serialize()
            storage = get_storage_class('xram_memory.utils.OverwriteDefaultStorage')()
            path = storage.save(FILE_PATH, ContentFile(json.dumps(serialized)))
    finally:
        if lock_info:
            logger.debug("lunr_index_rebuild: limpando o lock")
            logger.debug(lock_info)
            release_memcache_lock(*lock_info)
