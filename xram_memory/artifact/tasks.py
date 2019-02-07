from loguru import logger
from django.apps import apps
from celery import shared_task
from django.db.utils import IntegrityError


@shared_task
def add_additional_info_task(news_id, set_basic_info=False, fetch_archived_url=False, add_pdf_capture=False):
    # TODO: distribuir em dois grupos de tarefas separadas paralelas, executar cada grupo sequencialmente
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
        news.add_fetched_image()
        # setprogress... 4/5
        news.add_fetched_keywords()
        # setprogress... 5/5
        return True
    finally:
        if news:
            del news._inside_job


@shared_task
def bulk_insertion_task(urls, user_id):
    News = apps.get_model('artifact', 'News')
    User = apps.get_model('users', 'User')

    user = User.objects.get(pk=user_id)
    for url in urls:
        try:
            # 1) Crie uma notícia com o usuário informado
            news = News(url=url, created_by=user, modified_by=user)
            # 2) Salve a notícia
            news.save()
        except IntegrityError:
            # Não falhe uma tarefa se uma notícia já estiver cadastrada, simplesmente pule ela
            continue

    # TODO: Para cada url:
    # 3) Informe o status
