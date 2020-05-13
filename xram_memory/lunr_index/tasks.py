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
import requests
import json

FILE_PATH = settings.LUNR_INDEX_FILE_PATH
REBUILD_TIMEOUT = settings.LUNR_INDEX_REBUILD_TIMEOUT
REBUILD_INTERVAL = settings.LUNR_INDEX_REBUILD_INTERVAL
BACKEND = settings.LUNR_INDEX_BACKEND
SEARCH_FIELDS = settings.LUNR_INDEX_SEARCH_FIELDS
REMOTE_HOST = settings.LUNR_INDEX_REMOTE_HOST
REMOTE_SECRET = settings.LUNR_INDEX_REMOTE_SECRET
SAVE_DOCUMENT = settings.LUNR_INDEX_SAVE_DOCUMENT

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
            'uri': n.slug,
            'subjects': " ".join([k.name for k in n.subjects.all()]),
            'keywords': " ".join([k.name for k in n.keywords.all()]),
        } for n in News.objects.prefetch_related('keywords', 'subjects')
    ]
    #FIXME: não repetir ids
    items += [
        {
            'id': d.id,
            'title': d.name,
            'uri': d.document_id.hashid,
            'teaser': d.description,
            'subjects': " ".join([k.name for k in d.subjects.all()]),
            'keywords': " ".join([k.name for k in d.keywords.all()]),
        } for d in Documents.objects.prefetch_related('keywords', 'subjects')
            .filter(document_id__isnull=False)
            .filter(is_user_object=True)
            .filter(is_public=True)
    ]
    try:
        if (len(items)):
            if BACKEND == 'remote':
                with requests.post(REMOTE_HOST, json={
                    "documents": items,
                    "config": {
                        "searchFields": SEARCH_FIELDS,
                        "saveDocument": SAVE_DOCUMENT
                    }
                }, headers={
                    'Authorization': f'Bearer {REMOTE_SECRET}'
                }) as r:
                    r.raise_for_status()
            else:
                idx = lunr(
                    ref='id',
                    fields=[field for field in SEARCH_FIELDS if field != 'id'],
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
