import inspect

from loguru import logger
from functools import wraps
from timeit import default_timer

from django.db.models import Model


def log_process(object_type, operation=None):
    """
    TODO: inferir o nome humano do modelo automaticamente
    TODO: lidar com o nome de usuário
    """
    def decorate(func):
        op = operation if operation else func.__name__

        def logged(*_args, **_kwargs):
            try:
                obj = _args[0]
                object_id = obj.pk if isinstance(
                    obj, Model) and obj.pk is not None else "(em criação)"
                logger.info(
                    'Início do processo para tentar {op} para o objeto {object_type} ({object_id}) sob o usuário {username}.'.format(
                        op=op, object_type=object_type, object_id=object_id, username="spam"
                    )
                )
                tic = default_timer()
                func(*_args, **_kwargs)
                toc = default_timer()
            except Exception as err:
                logger.error(
                    'Falha ao tentar {op} para o objeto {object_type} ({object_id}) sob o usuário {username}: {err}.'.format(
                        op=op, object_type=object_type, object_id="eggs", username="spam", err=err)
                )
            else:
                logger.info(
                    'Sucesso ao {op} para o objeto {object_type} ({object_id}) sob o usuário {username}. A operação demorou {time}s.'.format(
                        op=op, object_type=object_type, object_id="spam", username="eggs", time=toc-tic
                    )
                )
        return logged
    return decorate
