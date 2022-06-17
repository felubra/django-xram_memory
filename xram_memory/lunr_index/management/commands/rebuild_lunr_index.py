from django.core.management.base import BaseCommand
from ...tasks import lunr_index_rebuild
from requests.exceptions import ConnectionError


class Command(BaseCommand):
    help = "Reconstrói o índice lunr"

    def handle(self, *args, **options):
        try:
            lunr_index_rebuild(None, True)
        except ConnectionError as exception:
            print(
                f"Falha enviar um {exception.request.method} para {exception.request.url}. "
                "Verifique se o backend remoto está rodando."
            )
        except (OSError, RuntimeError):
            print("Falha ao executar o comando")
        else:
            print("Índice construído com sucesso")
