import inspect

from loguru import logger
from functools import wraps
from timeit import default_timer
from functools import wraps

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

        @wraps(func)
        def logged(*_args, **_kwargs):
            try:
                obj = _args[0]
                try:
                    username = getattr(get_current_user(),
                                       'username', None)
                    if not username:
                        username = str(obj.modified_by)
                except:
                    username = '<anônimo>'
                object_id = obj.pk if (isinstance(
                    obj, Model) and obj.pk is not None) else "(em criação)"
                logger.info(
                    '[{username} - {object_id} - {object_type}] Início: {op}.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username
                    )
                )
                tic = default_timer()
                result = func(*_args, **_kwargs)
                toc = default_timer()
            except Exception as err:
                logger.error(
                    '[{username} - {object_id} - {object_type}] FALHA: {op}: {err}.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username
                    )
                )
            else:
                # TODO: informar se o processamento de func foi cacheado pela @lru_cache
                logger.info(
                    '[{username} - {object_id} - {object_type}] Término: {op}: {time:.2f} s.'.format(
                        op=op, object_type=object_type, object_id=object_id, username=username, time=toc-tic
                    )
                )
                return result
        return logged
    return decorate
