from django.core.management.base import BaseCommand
from xram_memory.artifact.models import Document


# TODO: opção para determinar apenas dos documentos que não tem mime_type
class Command(BaseCommand):
    help = "Determina o mimetype para todos os documentos no banco de dados"

    def handle(self, *args, **options):
        generated_count = 0
        for document in Document.objects.all():
            if document.determine_mime_type():
                document.save()
                generated_count += 1
        return "{} documentos tiveram mimetype populado".format(generated_count)
