from __future__ import absolute_import, unicode_literals
import os
import socket
from django.core.checks import register, Warning, Critical
from kombu import Connection
from kombu.exceptions import OperationalError
from django.conf import settings
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app


@register()
def celery_broker_check(app_configs, **kwargs):
    errors = []

    if os.environ['DJANGO_CONFIGURATION'] == 'Development':
        errors.append(
            Warning(
                'Pulando as verificações sobre o servidor de fila, pois estamos em desenvolvimento.',
                hint="Pode ser que o aplicativo não funcione corretamente"
            )
        )
        return errors

    try:
        conn = Connection(settings.CELERY_BROKER_URL)
        conn.ensure_connection(max_retries=3)
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            errors.append(
                Critical(
                    'Nenhum worker do Celery foi encontrado',
                    hint="Tenha certeza de que você iniciou ao menos um worker",
                    obj=inspect,
                    id='xram_memory.CeleryNoWorkerError',
                )
            )
    except (IOError, OperationalError):
        errors.append(
            Critical(
                'Falha ao tentar conexão com o message broker do Celery',
                hint='Verifique se o broker está rodando e disponível em {}.'.format(
                    settings.CELERY_BROKER_URL),
                obj=conn,
                id='xram_memory.CeleryBrokerConnectionError',
            )
        )
    return errors


__all__ = ('celery_app',)
