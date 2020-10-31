from tests.utils import basic_news
import tempfile
import pytest
import os
from lunr.index import Index
from .utils import without_elastic_search, without_artifact_auto_processing


@without_artifact_auto_processing()
@without_elastic_search()
@pytest.mark.last
@pytest.mark.django_db(transaction=True)
def test_localsearch_remote_elastic_lunr(settings, mocker):
    #FIXME: mocar os métodos de NewsFetcher
    settings.LUNR_INDEX_BACKEND = 'remote'
    settings.LUNR_INDEX_REMOTE_HOST = 'http://localhost:5000'
    settings.LUNR_INDEX_REMOTE_SECRET = 'alabamba'

    mocked_client = mocker.Mock()
    mocker.patch('xram_memory.lunr_index.lib.index_builders.RemoteElasticLunrIndexBuilder._get_client', return_value=mocked_client)
    mocker.patch('xram_memory.lunr_index.signals.celery_is_avaliable', return_value=False)


    with basic_news() as news:
        news.save()
        # verifique se a requisição foi chamada
        assert mocked_client.post.called
        mocked_client.post.called_with(
            settings.LUNR_INDEX_REMOTE_HOST,
            headers={'Authorization': f'Bearer {settings.LUNR_INDEX_REMOTE_SECRET}'}
        )


@without_artifact_auto_processing()
@without_elastic_search()
@pytest.mark.last
@pytest.mark.django_db(transaction=True)
def test_localsearch_lunr_py(settings, mocker):
    #FIXME: mocar os métodos de NewsFetcher
    settings.LUNR_INDEX_BACKEND = 'local'
    try:
        fd, file_path, = tempfile.mkstemp(dir=settings.MEDIA_ROOT)
        settings.LUNR_INDEX_FILE_PATH = file_path
        mocker.patch('xram_memory.lunr_index.signals.celery_is_avaliable', return_value=False)
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
            if (file_path):
                os.remove(file_path)
