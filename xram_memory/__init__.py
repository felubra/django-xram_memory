from __future__ import absolute_import, unicode_literals
from django.core.checks import register, Critical
from kombu.exceptions import OperationalError
from urllib3.exceptions import HTTPError
from elasticsearch import Elasticsearch
from django.conf import settings
from kombu import Connection
import tempfile
import os


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app


@register(deploy=True)
def celery_broker_check(app_configs, **kwargs):
    errors = []
    try:
        conn = Connection(settings.CELERY_BROKER_URL)
        conn.ensure_connection(max_retries=3)
        from celery.task.control import inspect

        insp = inspect()
        d = insp.stats()
        if not d:
            errors.append(
                Critical(
                    "Nenhum worker do Celery foi encontrado",
                    hint="Tenha certeza de que você iniciou ao menos um worker",
                    obj=inspect,
                    id="xram_memory.CeleryNoWorkerError",
                )
            )
    except (IOError, OperationalError):
        errors.append(
            Critical(
                "Falha ao tentar conexão com o message broker do Celery",
                hint="Verifique se o broker está rodando e disponível em {}.".format(
                    settings.CELERY_BROKER_URL
                ),
                obj=conn,
                id="xram_memory.CeleryBrokerConnectionError",
            )
        )
    return errors


@register()
def elastic_lunr_index_folder(app_configs, **kwargs):
    errors = []
    try:
        lunr_index_file_path = getattr(settings, "LUNR_INDEX_FILE_PATH", None)
        if lunr_index_file_path:
            lunr_index_file_folder = os.path.dirname(lunr_index_file_path)
            if not os.path.exists(lunr_index_file_folder):
                raise FileNotFoundError(
                    f"Falha ao verificar a pasta do arquivo de índice (elastic) lunr em: {lunr_index_file_folder}"
                )
    except FileNotFoundError as e:
        errors.append(
            Critical(
                str(e),
                hint="Verifique se a pasta existe e se o aplicativo tem acesso a ela.",
            )
        )

    return errors


@register(deploy=True)
def check_elastic_search(app_configs, **kwargs):
    errors = []
    try:
        elastic_host = settings.ELASTICSEARCH_DSL["default"]["hosts"]
        es = Elasticsearch(elastic_host, verify_certs=True)
        if not es.ping():
            raise ValueError("Connection failed")
    except (ValueError, HTTPError):
        errors.append(
            Critical(
                "Falha ao tentar conexão com o Elasticsearch",
                obj=es,
                id="xram_memory.ElasticSearchError",
            )
        )
    return errors


@register(deploy=True)
def check_libraries(app_configs, **kwargs):
    errors = []

    # cria um arquivo temporário e abre ele com a libmagic para verificar se a biblioteca está funcionando
    try:
        import magic

        with tempfile.TemporaryFile() as f:
            mimetype = magic.from_buffer(f.read(1024), mime=True)
    except:
        errors.append(
            Critical(
                "Biblioteca lib_magic não está funcional.",
                id="xram_memory.CheckLibrariesError",
            )
        )

    # gera um pdf de uma string para verificar se wkhtmltopdf está funcional
    try:
        import pdfkit

        result = pdfkit.from_string("teste", False)
        if not result:
            raise ValueError
    except:
        errors.append(
            Critical(
                "wkhtmltopdf não está funcional.",
                id="xram_memory.CheckLibrariesError",
            )
        )

    # importa o corpus do ntlk usado pelo newspaper3k para verificar se esse foi baixado
    try:
        from nltk.corpus import brown, movie_reviews, wordnet, stopwords
        from nltk.tokenize import punkt
    except ImportError as e:
        errors.append(
            Critical(
                "Falha ao importar nltk e/ou nltk corpora",
                id="xram_memory.CheckLibrariesError",
            )
        )

    return errors


__all__ = ("celery_app",)
