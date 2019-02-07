from loguru import logger
from django.apps import apps
from celery import shared_task, group
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


PROCESSING_TASK_TIMEOUT = 300
FETCH_TASK_TIMEOUT = 30


@shared_task(throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def add_pdf_capture_task(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        news.add_pdf_capture()
        news.save()
        return True
    finally:
        if news:
            del news._inside_job

# TODO: lidar com exceções: ValidationError
@shared_task(throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def set_basic_info_task(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        basic_info = news.set_basic_info()
        news.save()
        return basic_info
    finally:
        if news:
            del news._inside_job


@shared_task(time_limit=FETCH_TASK_TIMEOUT, rate_limit="60/m")
def fetch_archived_url_task(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        news.fetch_archived_url()
        news.save()
        return True
    finally:
        if news:
            del news._inside_job


# TODO: tratar exceção ValueError
@shared_task(time_limit=PROCESSING_TASK_TIMEOUT)
def add_news_task(url, user_id):
    News = apps.get_model('artifact', 'News')
    User = apps.get_model('users', 'User')

    try:
        user = User.objects.get(pk=user_id)
        # 1) Crie uma notícia com o usuário informado
        news = News(url=url, created_by=user, modified_by=user)
        # 2) Salve a notícia
        news.save()
        return True
    except IntegrityError:
        pass
