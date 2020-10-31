import os
import re
import magic
import datetime
from pathlib import Path
from loguru import logger
from kombu import Connection
from bs4 import BeautifulSoup
from django.conf import settings
from celery.five import monotonic
from django.db import transaction
from django.core.cache import cache
from contextlib import contextmanager
from functools import wraps, lru_cache
from django.contrib.staticfiles import finders
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from whitenoise.storage import CompressedManifestStaticFilesStorage
from django.core.files.storage import FileSystemStorage, DefaultStorage


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    Fonte: https://djangosnippets.org/snippets/690/

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': ("Certifique-se de que o arquivo enviado não seja maior do que %(max_size)s."
                     " O tamanho do seu arquivo é %(size)s."),
        'min_size': ("Certifique-se de que o arquivo enviado tenha pelo menos %(min_size)s. "
                     "O tamanho do seu arquivo é %(size)s."),
        'content_type': "Este tipo de arquivo (%(content_type)s) não é suportado.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                  'min_size', params)

        if self.content_types:
            # Leia os primeiros 1024 bytes dos dados para determinar seu tipo com a libmagic
            content_type = magic.from_buffer(data.read(1024), mime=True)
            data.file._mime_type = content_type
            data.seek(0)
            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)


class SignalException(Exception):
    pass


def celery_is_avaliable():
    try:
        conn = Connection(settings.CELERY_BROKER_URL)
        conn.ensure_connection(max_retries=3)
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            raise AttributeError
    except:
        return False
    else:
        return True


def task_on_commit(task, sync_context=False, sync_failback=True):
    """
    Executa uma tarefa após a execução de uma função decorada.
    A função decorada deve retornar um valor que será usado como argumento para a tarefa.
    Se função decorada invocar `SignalException` ou não retornar parâmetro algum, ela não será executada.
    """
    def decorate(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                task_args = func(*args, **kwargs)
            except SignalException:
                return

            if not task_args:
                return

            # TODO: cachear (?)
            execute_async = celery_is_avaliable()

            if execute_async:
                transaction.on_commit(lambda task_args=task_args:
                                      task.delay(*task_args))
            elif sync_failback and not execute_async:
                transaction.on_commit(lambda task_args=task_args, sync_context=sync_context:
                                      task(*task_args, sync=True) if sync_context else task(*task_args))
            else:
                raise RuntimeError(
                    "Falha ao executar {}: servidor de filas não está disponível.".format(func.__name__))
        return decorated
    return decorate


@lru_cache(maxsize=16)
def get_file_icon(icon_name):
    """ retorne o caminho completo de um ícone do pacote file-icon-vectors"""
    try:
        icon_file = finders.find(
            Path('file-icon-vectors/dist/icons/vivid/{icon}.svg'.format(icon=icon_name)))
        if icon_file is None:
            raise ValueError
        return icon_file
    except ValueError:
        return finders.find(
            Path('file-icon-vectors/dist/icons/vivid/blank.svg'))


class PatchedCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Override the replacement patterns to match URL-encoded quotations.
    Patch: https://code.djangoproject.com/ticket/21080#comment:12
    """
    manifest_strict = False
    patterns = (
        ("*.css", (
            r"""(url\((?:['"]|%22|%27){0,1}\s*(.*?)(?:['"]|%22|%27){0,1}\))""",
            (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
        )),
    )


class OverwriteStorageMixin(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    Fonte: https://gist.github.com/fabiomontefuscolo/1584462
    '''
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class OverwriteDefaultStorage(OverwriteStorageMixin, FileSystemStorage):
    """
    Classe que salva arquivo por cima do outro.
    """

def no_empty_html(value):
    """
    Um simples validador que converte html em texto para verificar se o texto não está em branco.
    """
    soup = BeautifulSoup(value, features="lxml")
    if not soup.get_text().strip():
        raise ValidationError(_('This field is required.'))

def release_memcache_lock(lock_id, timeout_at, status):
    logger.debug("release_memcache_lock: início da invocação")
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    if monotonic() < timeout_at and status:
        # don't release the lock if we exceeded the timeout
        # to lessen the chance of releasing an expired lock
        # owned by someone else
        # also don't release the lock if we didn't acquire it
        cache.delete(lock_id)
        logger.debug("release_fn: lock limpo")

@contextmanager
def memcache_lock(lock_id, oid, timeout, sync=True):
    """
    Gerenciador de contexto que garante a execução de apenas uma operação
    identificada por um lock_id e um timeout especificado, utilizando para isso
    uma trava definida via sistema de cache.
    Suporta operações síncronas ou assíncronas.
    Requer um sistema de cache distribuído que garanta a atomiciade de operações
    add().
    Em caso de operações asssíncronas, o usuário deve usar as informações do lock devolvidas
    no gerenciador de contexto para limpar a trava quando achar melhor.
    Retorna, via gerenciador de contexto, se a trava foi conseguida e suas informações.
    """
    timeout_at = monotonic() + timeout - 3
    # cache.add falha e retorna False se a entrada no cache já existir
    lock_acquired = cache.add(lock_id, oid, timeout)
    try:
        yield lock_acquired, (lock_id, timeout_at, lock_acquired,)
    finally:
        if sync:
            # Se a operação for síncrona, libere o lock agora, pois a operação já foi realizada
            release_memcache_lock(lock_id, timeout_at, lock_acquired)

def datetime_to_string(obj: datetime.datetime):
    if isinstance(obj, datetime.datetime):
        return str(obj)


# Exiba a toolbar apenas se requisição não for ajax
def show_toolbar(request):
    if request.is_ajax():
        return False
    return True