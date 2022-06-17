import requests
from xram_memory.lib.news_fetcher.plugins.base import ArchivePluginBase


class ArchiveORGArchiveFetcher(ArchivePluginBase):
    @staticmethod
    def fetch(url):
        """
        Verifica se existe adiciona a URL de uma versão arquivada desta notícia no `Internet Archive`
        """
        response = requests.get(
            "https://archive.org/wayback/available?url={}".format(url)
        )
        response.raise_for_status()
        response = response.json()
        available = archived_url = (
            response.get("archived_snapshots", {})
            .get("closest", {})
            .get("available", False)
        )
        if available:
            archived_url = (
                response.get("archived_snapshots", {}).get("closest", {}).get("url", "")
            )
            return archived_url
        return ""
