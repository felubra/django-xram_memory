from celery import group
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from retrying import retry
from urllib.parse import urlsplit
from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.utils import celery_is_avaliable
import random
import xram_memory.artifact.tasks as background_tasks


@receiver(post_save)
def set_mimetype_filesize_for_documents(sender, **kwargs):
    """
    Defina o tamanho e o tipo do arquivo para documentos.
    """
    instance = kwargs['instance']

    if hasattr(instance, '_save_in_signal'):
        return

    if isinstance(instance, (Document)):
        try:
            # TODO: otimizar as funções abaixo com lru_cache utilizando o hash do arquivo
            instance.determine_mime_type()
            instance.determine_file_size()
            # Adicione uma flag privada no modelo para evitar que esse handler execute
            # infinitamente, já que vamos chamar o save() aqui
            instance._save_in_signal = True
            instance.save()
        finally:
            del instance._save_in_signal


# TODO: mover para o modelo da notícia
def associate_newspaper(news_instance: News):
    """
    Com base na URL da notícia, associa ela com um jornal existente ou cria este jornal e faz a associação.
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
    Inspeciona uma tarefa do celery, que será executada sincronicamente, e emula o comportamento de tentativas dessa
    biblioteca.
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
        the_task(*arguments)

    retry_task(task, args)


def determine_additional_tasks_to_run(news_instance):
    """
    Com base nas opções definidas pelo usuário, determine quais tarefas de processamento adicional executar.
    """
    fields_and_task_info = {
        '_set_basic_info': (background_tasks.news_set_basic_info, (news_instance.pk, True)),
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
    instance = kwargs['instance']
    if hasattr(instance, '_save_in_signal'):
        return
    if isinstance(instance, News):
        # Se esta notícia não tem jornal, associe ela a um
        if not instance.newspaper:
            associate_newspaper(instance)

        tasks = determine_additional_tasks_to_run(instance)
        if len(tasks):
            if celery_is_avaliable():
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
