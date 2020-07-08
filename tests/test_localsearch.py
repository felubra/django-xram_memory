from tests.fixtures import NewsFactory
from tests.utils import basic_news
import requests_mock
import tempfile
import pytest
import json
import os
from lunr.index import Index
from .utils import without_elastic_search

@without_elastic_search()
@pytest.mark.last
@pytest.mark.django_db(transaction=True)
def test_localsearch_remote_elastic_lunr(settings):
    #FIXME: mocar os métodos de NewsFetcher
    settings.LUNR_INDEX_BACKEND = 'remote'
    settings.LUNR_INDEX_REMOTE_HOST = 'http://localhost:5000'
    settings.LUNR_INDEX_REMOTE_SECRET = 'alabamba'

    with requests_mock.Mocker() as m:
        m.register_uri('POST', settings.LUNR_INDEX_REMOTE_HOST, text='success')
        with basic_news() as news:
            news.save()
        # verifique se a requisição foi chamada
        assert m.called
        # verifique se foi enviada uma requisição para o servidor configurado
        reqs = [r for r in m.request_history if settings.LUNR_INDEX_REMOTE_HOST in r.url]
        assert len(reqs)

@without_elastic_search()
@pytest.mark.last
@pytest.mark.django_db(transaction=True)
def test_localsearch_lunr_py(settings):
    #FIXME: mocar os métodos de NewsFetcher
    settings.LUNR_INDEX_BACKEND = 'local'

    try:
        fd, file_path, = tempfile.mkstemp(dir=settings.MEDIA_ROOT)
        settings.LUNR_INDEX_FILE_PATH = file_path
        with basic_news() as news:
            news.save()
            with open(file_path, 'r') as json_index:
                data = json_index.read()
                idx = Index.load(data)
                assert len(idx.search(news.title))
    finally:
        try:
            os.close(fd)
        finally:
            os.remove(file_path)
