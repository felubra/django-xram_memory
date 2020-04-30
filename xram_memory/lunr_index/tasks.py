from celery import shared_task, group
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

SETTINGS = settings.LUNR_INDEX
REBUILD_TIMEOUT = SETTINGS['REBUILD_TIMEOUT']
REBUILD_INTERVAL = SETTINGS['REBUILD_INTERVAL']

@shared_task(
    retry_backoff=5,
    max_retries=3,
    retry_backoff_max=REBUILD_TIMEOUT / 4,
    eta = now() + timedelta(seconds=REBUILD_INTERVAL),
    retry_jitter=True,
    time_limit=REBUILD_TIMEOUT
)
def lunr_index_rebuild():
    pass