""" Implementa a geração de índices de busca locais com a biblioteca lunr.py
ou através do envio a um serviço remoto """

import json
from itertools import chain

from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from django.apps import apps

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from lunr import lunr
from loguru import logger

from xram_memory.utils import datetime_to_string


class LocalSearchIndexBuilder:
    @classmethod
    def _prepare_documents_for_indexing(cls, flat_taxonomy=False):
        """
        Obtém e prepara uma lista com os artefatos (Notícias e Documentos) para serem indexados.
        """
        News = apps.get_model("artifact", "News")
        Documents = apps.get_model("artifact", "Document")
        documents_to_index = []

        news_queryset = News.objects.prefetch_related("keywords", "subjects")
        documents_queryset = (
            Documents.objects.prefetch_related("keywords", "subjects")
            .filter(document_id__isnull=False)
            .filter(is_user_object=True)
            .filter(is_public=True)
        )

        # Gere uma lista com as notícias e os documentos, com campos em comum
        for idx, item in enumerate(chain(news_queryset, documents_queryset)):
            try:
                subjects = [k.name for k in item.subjects.all()]
                keywords = [k.name for k in item.keywords.all()]

                if flat_taxonomy:
                    subjects = " ".join(subjects)
                    keywords = " ".join(keywords)

                index_document = {
                    "id": item.id,
                    "type": "news" if isinstance(item, News) else "document",
                    "thumbnail": item.thumbnail,
                    "subjects": subjects,
                    "keywords": keywords,
                }
                if isinstance(item, News):
                    # use a data de publicação da notícia ou, caso não haja esta informação, a data de modificação
                    # em seu lugar
                    index_document["published_date"] = (
                        datetime_to_string(item.published_date)
                        if item.published_date is not None
                        else datetime_to_string(item.modified_at)
                    )
                    index_document["title"] = item.title
                    index_document["teaser"] = item.teaser
                    index_document["uri"] = item.slug
                    if getattr(item, "newspaper", None):
                        index_document["newspaper"] = {
                            "title": item.newspaper.title,
                            "favicon_logo": item.newspaper.favicon_logo,
                            "url": item.newspaper.url,
                        }
                else:
                    index_document["published_date"] = datetime_to_string(
                        item.uploaded_at
                    )
                    index_document["newspaper"] = None
                    index_document["title"] = item.name
                    index_document["uri"] = item.document_id.hashid
                    index_document["teaser"] = item.description
                documents_to_index.append(index_document)
            except Exception as e:
                logger.debug(
                    "Falha ao construir um objeto {} para indexação local, com o id {}: {}".format(
                        item.verbose_name, item.pk, e
                    )
                )
        return documents_to_index


class LunrIndexBuilder(LocalSearchIndexBuilder):
    @classmethod
    def build(cls, output_file_path: str):
        documents_to_index = cls._prepare_documents_for_indexing(True)
        idx = lunr(
            ref="id",
            fields=[field for field in documents_to_index[0].keys() if field != "id"],
            documents=documents_to_index,
            languages=["pt", "en"],
        )
        serialized = idx.serialize()
        storage = get_storage_class("xram_memory.utils.OverwriteDefaultStorage")()
        return storage.save(output_file_path, ContentFile(json.dumps(serialized)))


class RemoteElasticLunrIndexBuilder(LocalSearchIndexBuilder):
    @classmethod
    def _get_client(cls, retry=True):
        if retry:
            retry_strategy = Retry(
                total=5,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
                backoff_factor=5,
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
        else:
            adapter = HTTPAdapter()
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    @classmethod
    def build(
        cls,
        remote_url: str,
        remote_secret: str,
        search_fields: list,
        save_document=True,
        retry=True,
    ):
        documents_to_index = cls._prepare_documents_for_indexing()
        http = cls._get_client(retry)
        with http.post(
            remote_url,
            json={
                "documents": documents_to_index,
                "config": {
                    "searchFields": search_fields,
                    "saveDocument": save_document,
                },
            },
            headers={"Authorization": f"Bearer {remote_secret}"},
        ) as response:
            response.raise_for_status()
            return response.ok
