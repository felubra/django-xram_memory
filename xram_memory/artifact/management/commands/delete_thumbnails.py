from xram_memory.artifact.models import Document, NewsImageCapture, NewsPDFCapture
from django.core.management.base import BaseCommand
from easy_thumbnails.files import get_thumbnailer


def delete_thumbnails_for_model(model, field=None):
    files_deleted = 0

    for instance in model.objects.all():
        if field is not None:
            thumbnailer = get_thumbnailer(getattr(instance, field).file)
        else:
            thumbnailer = get_thumbnailer(instance.file)
        files_deleted += thumbnailer.delete_thumbnails()
    return "{} miniaturas de {} excluídas.".format(files_deleted, model._meta.verbose_name.title())


class Command(BaseCommand):
    help = 'Apaga os thumbnails criados para modelos do app Artifact'
    SUPORTED_MODELS_AND_FIELDS = (
        (NewsImageCapture, 'image_document'),
        (NewsPDFCapture, 'pdf_document'),
        (Document,)
    )

    def handle(self, *args, **options):
        for model_and_field in self.SUPORTED_MODELS_AND_FIELDS:
            self.stdout.write(self.style.SUCCESS(
                delete_thumbnails_for_model(*model_and_field)))
