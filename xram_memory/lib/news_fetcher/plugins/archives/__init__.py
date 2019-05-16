import requests
from xram_memory.lib.news_fetcher.plugin import ArchiveNewsFetcherPlugin


class ArchiveORGArchiveFetcher(ArchiveNewsFetcherPlugin):
    @staticmethod
    def fetch(url):
        """
        Verifica se existe adiciona a URL de uma versão arquivada desta notícia no `Internet Archive`
        """
        try:
            response = requests.get(
                "https://archive.org/wayback/available?url={}".format(url))
            response.raise_for_status()
            response = response.json()

            if (response["archived_snapshots"] and response["archived_snapshots"]["closest"] and
                    response["archived_snapshots"]["closest"]["available"]):
                closest_archive = response["archived_snapshots"]["closest"]
                return closest_archive["url"]
            return ''
        except:
            return ''
