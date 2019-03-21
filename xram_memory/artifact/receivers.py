from xram_memory.artifact.models import News, Newspaper
import xram_memory.artifact.tasks as background_tasks
from xram_memory.utils import celery_is_avaliable
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from urllib.parse import urlsplit
from retrying import retry
from celery import group
import random


# TODO: mover para o modelo da notícia
def associate_newspaper(news_instance: News):
    """
    Com base na URL da notícia, associa ela com um jornal existente ou cria este jornal e, por fim, faz a associação.
    """
    news_instance._save_in_signal = True
    try:
        base_url = "{uri.scheme}://{uri.netloc}".format(
            uri=urlsplit(news_instance.url))
        news_instance.newspaper = Newspaper.objects.get(url=base_url)
        news_instance.save()
    except Newspaper.DoesNotExist:
        # crie um jornal (newspaper ) básico agora
        newspaper = None
        try:
            newspaper = Newspaper.objects.create(
                title=base_url,
                url=base_url,
                created_by=news_instance.created_by,
                modified_by=news_instance.modified_by
            )
        except:
            pass
        else:
            news_instance.newspaper = newspaper
            news_instance.save()
    finally:
        del news_instance._save_in_signal


def try_task(task, args):
    """
    Emula o comportamento de tentar novamente do celery para uma tarefas que será executada sincronicamente.
    """
    expect_to_throw = tuple(getattr(task, 'throws', ()))
    autoretry_for = tuple(getattr(task, 'autoretry_for', ()))
    stop_max_attempt_number = 3
    wait_exponential_multiplier = 1000
    wait_exponential_max = 30 * 1000

    def need_to_retry_for(exception):
        return isinstance(exception, autoretry_for)

    @retry(stop_max_attempt_number=stop_max_attempt_number,
           retry_on_exception=need_to_retry_for, wait_exponential_multiplier=wait_exponential_multiplier,
           wait_exponential_max=wait_exponential_max)
    def retry_task(the_task, arguments):
        try:
            the_task(*arguments)
        except Exception as e:
            if isinstance(e, expect_to_throw):
                pass
            else:
                raise

    retry_task(task, args)


def determine_additional_tasks_to_run(news_instance, execute_async=True):
    """
    Com base nas opções definidas pelo usuário, determine quais tarefas de processamento adicional executar.
    """
    fields_and_task_info = {
        '_set_basic_info': (background_tasks.news_set_basic_info, (news_instance.pk, not execute_async)),
        '_fetch_archived_url': (background_tasks.news_add_archived_url, (news_instance.pk,)),
        '_add_pdf_capture': (background_tasks.news_add_pdf_capture, (news_instance.pk,)),
    }
    tasks = []

    for field, task_info in fields_and_task_info.items():
        if getattr(news_instance, field, False):
            tasks.append(task_info)

    return tasks

# Sinais para o processamento de News
@receiver(post_save)
def news_additional_processing(sender, **kwargs):
    """
    De acorodo com as opções selecionadas pelo usuário, executa ou agenda tarefas para obter informações adicionais
    sobre determinada Notícia.
    """
    instance = kwargs['instance']
    if hasattr(instance, '_save_in_signal'):
        return
    if isinstance(instance, News):
        # Se esta notícia não tem jornal, associe ela a um
        if not instance.newspaper:
            associate_newspaper(instance)

        execute_async = celery_is_avaliable()
        tasks = determine_additional_tasks_to_run(instance, execute_async)
        if len(tasks):
            if execute_async:
                transaction.on_commit(lambda instance=instance, tasks=tasks: group(
                    [task.s(*args) for task, args in tasks]).apply_async()
                )
            else:
                for task, args in tasks:
                    transaction.on_commit(
                        lambda task=task, args=args: try_task(task, args))


# Sinais para o processamento de Newspaper
@receiver(post_save)
def newspaper_additional_processing(sender, **kwargs):
    """
    Agenda ou executa tarefa para obter informações básicas sobre um Jornal.
    """
    instance = kwargs['instance']
    if hasattr(instance, '_save_in_signal'):
        return
    if isinstance(instance, Newspaper) and not instance.has_basic_info:
        if celery_is_avaliable():
            transaction.on_commit(
                lambda instance=instance: background_tasks.newspaper_set_basic_info.delay(instance.pk))
        else:
            transaction.on_commit(
                lambda instance=instance: try_task(background_tasks.newspaper_set_basic_info, (instance.pk,)))
