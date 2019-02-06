from loguru import logger
from django.apps import apps
from celery import shared_task


@shared_task
def add_additional_info(news_id, set_basic_info=False, fetch_archived_url=False, add_pdf_capture=False):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        if set_basic_info:
            news.set_basic_info()
        # setprogress... 1/3
        if fetch_archived_url:
            news.fetch_archived_url()
        # setprogress... 2/3
        news.save()
        if add_pdf_capture:
            news.add_pdf_capture()
        # setprogress... 3/3
        if not news.image_capture and hasattr(news, '_image') and len(news._image) > 0:
            news.add_fetched_image()
        # setprogress... 4/5
        news.add_fetched_keywords()
        # setprogress... 5/5
        return True
    finally:
        if news:
            del news._inside_job
