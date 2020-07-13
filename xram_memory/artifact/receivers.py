from xram_memory.artifact.models import Document, News, Newspaper
import xram_memory.artifact.tasks as background_tasks
from xram_memory.utils import celery_is_avaliable
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from urllib.parse import urlsplit
from retrying import retry
from celery import group
import random
from xram_memory.utils.decorators import disable_for_loaddata
from xram_memory.utils.classes import SignalProcessor

class TaskOrientedSignalProcessor(SignalProcessor):
    def _determine_additional_tasks_to_run(self, fields_and_tasks_info, instance):
        """
        Com base nas opções definidas pelo usuário, determine quais tarefas de processamento adicional executar.
        """
        tasks = []

        for field, task_info in fields_and_tasks_info.items():
            if getattr(instance, field, False):
                tasks.append(task_info)
        return tasks

    def _try_task(self, task, args):
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

class DocumentSignalProcessor(SignalProcessor):
    def __init__(self):
        self.models = [Document]
        self.signals = [post_save]
        super().__init__()

    @disable_for_loaddata
    def handler(self, *args, **kwargs):
        """
        Defina o mimetype do arquivo para documentos e seu document_id.
        """
        instance = kwargs['instance']

        if hasattr(instance, '_save_in_signal'):
            return

        if isinstance(instance, (Document)):
            try:
                got_document_id = instance.set_document_id()
                got_new_mime_type = instance.determine_mime_type()
                # Somente salve o modelo se de fato ao menos uma operação foi executada com sucesso
                if got_document_id or got_new_mime_type:
                    # Adicione uma flag privada no modelo para evitar que esse handler execute
                    # de novo, já que vamos salvar o modelo novamente aqui
                    instance._save_in_signal = True
                    instance.save()
            finally:
                if hasattr(instance, '_save_in_signal'):
                    del instance._save_in_signal


class NewsSignalProcessor(TaskOrientedSignalProcessor):
    def __init__(self):
        self.models = [News]
        self.signals = [post_save]
        super().__init__()

    # TODO: mover para o modelo da notícia
    def _associate_newspaper(self, news_instance: News):
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


    @disable_for_loaddata
    def handler(self, sender, **kwargs):
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
                self._associate_newspaper(instance)

            execute_async = celery_is_avaliable()
            fields_and_tasks_info = {
                '_set_basic_info': (background_tasks.news_set_basic_info, (instance.pk, not execute_async)),
                '_fetch_archived_url': (background_tasks.news_add_archived_url, (instance.pk,)),
                '_add_pdf_capture': (background_tasks.news_add_pdf_capture, (instance.pk,)),
            }
            tasks = self._determine_additional_tasks_to_run(
                fields_and_tasks_info, instance)
            if len(tasks):
                if execute_async:
                    transaction.on_commit(lambda instance=instance, tasks=tasks: group(
                        [task.s(*args) for task, args in tasks]).apply_async()
                    )
                else:
                    for task, args in tasks:
                        transaction.on_commit(
                            lambda task=task, args=args: self._try_task(task, args))


class NewspaperSignalProcessor(TaskOrientedSignalProcessor):
    def __init__(self):
        self.signals=[post_save]
        self.models=[Newspaper]
        super().__init__()

    @disable_for_loaddata
    def handler(self, sender, **kwargs):
        """
        Agenda ou executa tarefa para obter informações básicas sobre um Jornal.
        """
        instance = kwargs['instance']
        if hasattr(instance, '_save_in_signal'):
            return
        if isinstance(instance, Newspaper):
            execute_async = celery_is_avaliable()
            fields_and_tasks_info = {
                '_set_basic_info': (background_tasks.newspaper_set_basic_info, (instance.pk,)),
                '_fetch_logo': (background_tasks.newspaper_set_logo_from_favicon, (instance.pk,)),
            }
            tasks = self._determine_additional_tasks_to_run(
                fields_and_tasks_info, instance)

            # esse sinal não veio de um formulário administrativo
            if not tasks and not hasattr(
                    instance, '_set_basic_info') and not instance.has_basic_info:
                tasks.append(fields_and_tasks_info['_set_basic_info'])

            if execute_async:
                transaction.on_commit(lambda instance=instance, tasks=tasks: group(
                    [task.s(*args) for task, args in tasks]).apply_async()
                )
            else:
                for task, args in tasks:
                    transaction.on_commit(
                        lambda task=task, args=args: self._try_task(task, args))
