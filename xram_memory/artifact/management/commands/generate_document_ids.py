from django.core.management.base import BaseCommand
from xram_memory.artifact.models import Document


class Command(BaseCommand):
    help = "Gera document_id para todos os documentos sem no banco de dados"

    def handle(self, *args, **options):
        generated_count = 0
        for document in Document.objects.all():
            if document.set_document_id():
                document.save()
                generated_count += 1
        return "{} documentos tiveram document_id gerado".format(generated_count)
