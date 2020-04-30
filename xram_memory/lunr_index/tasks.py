from celery import shared_task, group
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from django.apps import apps
import json
from lunr import lunr
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile


SETTINGS = settings.LUNR_INDEX
REBUILD_TIMEOUT = SETTINGS['REBUILD_TIMEOUT']
REBUILD_INTERVAL = SETTINGS['REBUILD_INTERVAL']
FILE_PATH = SETTINGS['FILE_PATH']

@shared_task(
    retry_backoff=5,
    max_retries=3,
    retry_backoff_max=REBUILD_TIMEOUT / 4,
    eta = now() + timedelta(seconds=REBUILD_INTERVAL),
    retry_jitter=True,
    time_limit=REBUILD_TIMEOUT
)
def lunr_index_rebuild():
    # Construa um índice com documentos e notícias
    # TODO: otimizar

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

    if (len(items)):
        idx = lunr(
            ref='id',
            fields=[k for k in items[0].keys() if k != 'id'],
            documents=items, languages=['pt','en']
        )
        serialized = idx.serialize()
        storage = get_storage_class('xram_memory.utils.OverwriteDefaultStorage')()
        path = storage.save(FILE_PATH, ContentFile(json.dumps(serialized)))