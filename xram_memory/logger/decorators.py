import inspect

from loguru import logger
from functools import wraps
from timeit import default_timer

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

from django.db.models import Model


def log_process(object_type, operation=None):
    """
    TODO: inferir o nome humano do modelo automaticamente
    TODO: refatorar para dar mais robustez (blocos try)
    """
    def decorate(func):
        op = operation if operation else func.__name__

        def logged(*_args, **_kwargs):
            try:
                username = getattr(get_current_user(), 'username', '<anônimo>')
                obj = _args[0]
                object_id = obj.pk if (isinstance(
                    obj, Model) and obj.pk is not None) else "(em criação)"
                logger.info(
                    'Início do processo para tentar {op} para o objeto {object_type} ({object_id}) sob o usuário {username}.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username
                    )
                )
                tic = default_timer()
                result = func(*_args, **_kwargs)
                toc = default_timer()
            except Exception as err:
                logger.error(
                    'Falha ao tentar {op} para o objeto {object_type} ({object_id}) sob o usuário {username}: {err}.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username, err=err)
                )
            else:
                # TODO: informar se o processamento de func foi cacheado pela @lru_cache
                logger.info(
                    'Sucesso ao {op} para o objeto {object_type} ({object_id}) sob o usuário {username}. A operação demorou {time:.2f} segundos.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username, time=toc-tic
                    )
                )
                return result
        return logged
    return decorate
