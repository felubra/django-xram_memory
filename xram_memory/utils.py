import re

from functools import wraps, lru_cache
from inspect import getfullargspec
from whitenoise.storage import CompressedManifestStaticFilesStorage

import magic

from kombu import Connection
from django.conf import settings
from django.db import transaction
from kombu.exceptions import OperationalError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.contrib.staticfiles import finders


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


# retorne o caminho completo de um ícone do pacote file-icon-vectors
def get_file_icon(icon_name):
    try:
        icon_file = finders.find(
            'file-icon-vectors/dist/icons/vivid/{icon}.svg'.format(icon=icon_name))
        if icon_file is None:
            raise ValueError
        return icon_file
    except ValueError:
        return finders.find(
            'file-icon-vectors/dist/icons/vivid/BLANK.svg'.format(icon=icon_name))


class PatchedCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    Override the replacement patterns to match URL-encoded quotations.
    Patch: https://code.djangoproject.com/ticket/21080#comment:12
    """
    patterns = (
        ("*.css", (
            r"""(url\((?:['"]|%22|%27){0,1}\s*(.*?)(?:['"]|%22|%27){0,1}\))""",
            (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
        )),
    )
