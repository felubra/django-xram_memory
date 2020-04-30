from celery import shared_task, group

@shared_task()
def lunr_index_rebuild():
    pass