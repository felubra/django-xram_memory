from xram_memory.utils import memcache_lock, release_memcache_lock, datetime_to_string
from xram_memory.lunr_index.util import LunrBackendValue
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from celery import shared_task, group
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from django.apps import apps
from itertools import chain
from loguru import logger
from lunr import lunr
import requests
import json

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
        News = apps.get_model('artifact', 'News')
        Documents = apps.get_model('artifact', 'Document')

        documents_to_index = []

        news_queryset = News.objects.prefetch_related('keywords', 'subjects')
        documents_queryset = (Documents.objects.prefetch_related('keywords', 'subjects')
                .filter(document_id__isnull=False)
                .filter(is_user_object=True)
                .filter(is_public=True))

        # Gere uma lista com as notícias e os documentos, com campos em comum
        for idx, item in enumerate(chain(news_queryset, documents_queryset)):
            try:
                subjects = [k.name for k in item.subjects.all()]
                keywords = [k.name for k in item.keywords.all()]

                if BACKEND == LunrBackendValue.BACKEND_LOCAL:
                    # o backend lunr.py não suporta lista como tipo de campo indexável
                    subjects = " ".join(subjects)
                    keywords = " ".join(keywords)

                index_document = {
                    'id': idx,
                    'type': 'news' if isinstance(item, News) else 'document',
                    'thumbnail': item.thumbnail,
                    'subjects': subjects,
                    'keywords': keywords,
                }
                if isinstance(item, News):
                    index_document['published_date'] = datetime_to_string(item.published_date)
                    index_document['title'] = item.title
                    index_document['teaser'] = item.teaser
                    index_document['uri'] = item.slug
                    index_document['newspaper'] = {
                        'title': item.newspaper.title,
                        'favicon_logo': item.newspaper.favicon_logo,
                        'url': item.newspaper.url,
                    }
                else:
                    index_document['published_date'] = datetime_to_string(item.uploaded_at)
                    index_document['newspaper'] = None
                    index_document['title'] = item.name
                    index_document['uri'] = item.document_id.hashid
                    index_document['teaser'] = item.description
                documents_to_index.append(index_document)
            except Exception as e:
                logger.debug("Falha ao indexar um(a) {}, com o id {}: {}"
                    .format(item.verbose_name, item.pk, e)
                )


        if BACKEND == LunrBackendValue.BACKEND_REMOTE:
            with requests.post(REMOTE_HOST, json={
                "documents": documents_to_index,
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
                documents=documents_to_index, languages=['pt','en']
            )
            serialized = idx.serialize()
            storage = get_storage_class('xram_memory.utils.OverwriteDefaultStorage')()
            path = storage.save(FILE_PATH, ContentFile(json.dumps(serialized)))
    finally:
        if lock_info:
            logger.debug("lunr_index_rebuild: limpando o lock")
            logger.debug(lock_info)
            release_memcache_lock(*lock_info)
