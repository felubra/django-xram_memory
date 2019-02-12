from loguru import logger
from django.apps import apps
from celery import shared_task, group
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError


PROCESSING_TASK_TIMEOUT = 300
FETCH_TASK_TIMEOUT = 30


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def add_additional_info(news_id, set_basic_info, fetch_archived_url, add_pdf_capture):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        if set_basic_info:
            news.set_basic_info()
            if getattr(news, '_image', None):
                add_image_for_news.delay(news._image, news_id)
            if getattr(news, '_keywords', None):
                add_keywords_for_news.delay(news._keywords, news_id)
        if fetch_archived_url:
            news.fetch_archived_url()
        if add_pdf_capture:
            add_pdf_capture_task.delay(news_id)

        # TODO: inclua add_image_for_news, add_keywords_for_news e add_pdf_capture_task num grupo e, quando elas terminarem, agende uma tarefa de indexação
        news.save()
        return news.pk
    finally:
        if news:
            del news._inside_job


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True,)
def add_keywords_for_news(keywords, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    news._keywords = keywords
    news.add_fetched_keywords()
    return True


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True,)
def add_image_for_news(image_url, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    news._image = image_url
    news.add_fetched_image()
    return True


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def add_pdf_capture_task(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    news.add_pdf_capture()
    return True

# TODO: tratar exceção ValueError
# TODO: adicionar um registro de inserção na interface administrativa
@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, time_limit=PROCESSING_TASK_TIMEOUT)
def add_news_task(url, user_id):
    News = apps.get_model('artifact', 'News')
    User = apps.get_model('users', 'User')
    try:
        # TODO: fazer um chain para invocar as outras chamadas aqui: set_basic_info & fetch_archived_url => add_pdf_capture, add_keywords, add_feched image
        user = User.objects.get(pk=user_id)
        # 1) Crie uma notícia com o usuário informado
        news = News(url=url, created_by=user, modified_by=user)
        # 2) Salve a notícia
        news.save()
        return news.pk
    # TODO: verificar por que a exceção IntegrityError não está sendo ignorada pelo parâmetro throws na tarefa
    except IntegrityError:
        pass
