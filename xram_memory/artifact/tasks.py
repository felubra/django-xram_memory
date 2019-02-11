from loguru import logger
from django.apps import apps
from celery import shared_task, group
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError


PROCESSING_TASK_TIMEOUT = 300
FETCH_TASK_TIMEOUT = 30


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
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


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, throws=(ValidationError,), time_limit=PROCESSING_TASK_TIMEOUT, rate_limit="10/m")
def set_basic_info_task(news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    try:
        news._inside_job = True
        basic_info = news.set_basic_info()

        try:
            # faça uma pré-validação do modelo aqui
            news.full_clean()
        except ValidationError as err:
            # ignore qualquer data de publicação fora do padrão que Fetcher trouxer
            if err.error_dict.get("published_date"):
                setattr(news, "published_date", None)
                del err.error_dict["published_date"]
            # se mesmo depois de tratarmos nossos erros aqui, ainda assim houver outros erros,
            # invoque uma exceção
            if len(err.error_dict.keys()) > 0:
                raise

        news.save()

        if hasattr(news, '_keywords') and len(news._keywords) > 0:
            add_keywords_for_news.apply_async(args=[news._keywords, news_id])
        if hasattr(news, '_image') and len(news._image) > 0:
            add_image_for_news.apply_async(args=[news._image, news_id])
        return basic_info
    finally:
        if news:
            del news._inside_job


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True,)
def add_keywords_for_news(keywords, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    news._keywords = keywords
    try:
        news._inside_job = True
        news.add_fetched_keywords()
        return True
    finally:
        if news:
            del news._inside_job


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True,)
def add_image_for_news(image_url, news_id):
    News = apps.get_model('artifact', 'News')
    news = News.objects.get(pk=news_id)
    news._image = image_url
    try:
        news._inside_job = True
        news.add_fetched_image()
        return True
    finally:
        if news:
            del news._inside_job


@shared_task(autoretry_for=(OperationalError,), retry_backoff=5, retry_kwargs={'max_retries': 10}, retry_backoff_max=300, retry_jitter=True, time_limit=FETCH_TASK_TIMEOUT, rate_limit="60/m")
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
        return True
    # TODO: verificar por que a exceção IntegrityError não está sendo ignorada pelo parâmetro throws na tarefa
    except IntegrityError:
        pass
