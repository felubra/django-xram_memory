from urllib.parse import urlsplit

from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save

import xram_memory.artifact.tasks as background_tasks
from xram_memory.artifact.models import Document, News, Newspaper


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


@receiver(post_save)
def news_add_newspaper(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, '_save_in_signal_add_newspaper'):
        return
    if isinstance(instance, (News)) and not instance.newspaper:
        instance._save_in_signal_add_newspaper = True
        try:
            base_url = "{uri.scheme}://{uri.netloc}".format(
                uri=urlsplit(instance.url))
            instance.newspaper = Newspaper.objects.get(url=base_url)
            instance.save()
        except Newspaper.DoesNotExist:
            # crie um jornal (newspaper ) básico agora
            newspaper = None
            try:
                newspaper = Newspaper.objects.create(
                    title=base_url,
                    url=base_url,
                    created_by=instance.created_by,
                    modified_by=instance.modified_by
                )
            except:
                pass
            else:
                instance.newspaper = newspaper
                instance.save()
        finally:
            del instance._save_in_signal_add_newspaper


@receiver(post_save)
def newspaper_add_basic_info(sender, **kwargs):
    instance = kwargs['instance']
    # Não entre em loop infinito
    if hasattr(instance, '_save_in_signal_newspaper_add_basic_info'):
        return
    if isinstance(instance, (Newspaper)) and not instance.has_basic_info:
        transaction.on_commit(lambda instance=instance: background_tasks.newspaper_set_basic_info.delay(
            instance.pk))


@receiver(post_save)
def news_add_basic_info(sender, **kwargs):
    instance = kwargs['instance']
    # Não agende a captura em pdf se o sinal foi enviado durante o cadastro de um jornal
    if hasattr(instance, '_save_in_signal_add_newspaper'):
        return
    if isinstance(instance, (News)) and getattr(instance, '_set_basic_info', False):
        transaction.on_commit(lambda instance=instance:
                              background_tasks.news_set_basic_info.delay(instance.pk))


@receiver(post_save)
def news_add_archived_url(sender, **kwargs):
    instance = kwargs['instance']
    # Não agende a captura em pdf se o sinal foi enviado durante o cadastro de um jornal
    if hasattr(instance, '_save_in_signal_add_newspaper'):
        return
    if isinstance(instance, (News)) and getattr(instance, '_fetch_archived_url', False):
        transaction.on_commit(lambda instance=instance:
                              background_tasks.news_add_archived_url.delay(instance.pk))


@receiver(post_save)
def news_add_pdf_capture(sender, **kwargs):
    instance = kwargs['instance']
    # Não agende a captura em pdf se o sinal foi enviado durante o cadastro de um jornal
    if hasattr(instance, '_save_in_signal_add_newspaper'):
        return
    if isinstance(instance, (News)) and getattr(instance, '_add_pdf_capture', False):
        transaction.on_commit(lambda instance=instance:
                              background_tasks.news_add_pdf_capture.delay(instance.pk))
