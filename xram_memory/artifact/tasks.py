from celery import group
from loguru import logger
from django.apps import apps
from django.db import transaction
from celery import shared_task, group
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError


PROCESSING_TASK_TIMEOUT = 300
FETCH_TASK_TIMEOUT = 30


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def newspaper_set_basic_info(newspaper_id):
    Newspaper = apps.get_model('artifact', 'Newspaper')
    newspaper = Newspaper.objects.get(pk=newspaper_id)
    newspaper._save_in_signal_newspaper_add_basic_info = True
    try:
        newspaper.set_basic_info()
        newspaper.save()
    except:
        raise
    else:
        return newspaper
    finally:
        del newspaper._save_in_signal_newspaper_add_basic_info


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError, ValueError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def news_set_basic_info(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news.set_basic_info()
        news.save()

        if getattr(news, '_image', None):
            add_image_for_news.delay(news._image, news_id)
        if getattr(news, '_keywords', None):
            add_keywords_for_news.delay(news._keywords, news_id)
    except:
        raise
    else:
        return news


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def news_add_archived_url(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news.fetch_archived_url()
        news.save()
    except:
        raise
    else:
        if news.archived_news_url:
            return news.archived_news_url
        else:
            return True


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, rate_limit="10/m",)
def add_keywords_for_news(keywords, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._keywords = keywords
        news.add_fetched_keywords()
    except:
        raise
    else:
        return True


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True,)
def add_image_for_news(image_url, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._image = image_url
        news.add_fetched_image()
        return news.image_capture
    except:
        raise
    else:
        return True


@shared_task(throws=(OSError,), autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def news_add_pdf_capture(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news.add_pdf_capture()
    except:
        raise
    else:
        return True

# TODO: tratar exceção ValueError
# TODO: adicionar um registro de inserção na interface administrativa
@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, max_retries=10, retry_backoff_max=300, retry_jitter=True, time_limit=PROCESSING_TASK_TIMEOUT)
def add_news_task(url, user_id):
    News = apps.get_model('artifact', 'News')
    User = apps.get_model('users', 'User')
    try:
        user = User.objects.get(pk=user_id)
        # 1) Crie uma notícia com o usuário informado
        news = News(url=url, created_by=user, modified_by=user)
        # 2) Salve a notícia
        news.save()
        # 3) Agende trabalhos para obter informações adicionais
        transaction.on_commit(lambda news=news: group([news_set_basic_info.s(
            news.pk), news_add_archived_url.s(news.pk), news_add_pdf_capture.s(news.pk)]).apply_async())
        return news.pk
    # TODO: verificar por que a exceção IntegrityError não está sendo ignorada pelo parâmetro throws na tarefa
    except IntegrityError:
        pass
    except:
        raise
