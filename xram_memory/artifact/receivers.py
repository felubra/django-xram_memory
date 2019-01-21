from django.dispatch import receiver
from django.db.models.signals import post_save

from xram_memory.artifact.models import Document, ImageDocument, PDFDocument


@receiver(post_save)
def set_mimetype_filesize(sender, **kwargs):
    instance = kwargs['instance']

    if hasattr(instance, '_save_in_signal'):
        return

    if isinstance(instance, (ImageDocument, PDFDocument,)):
        try:
            # TODO: otimizar com lru_cache utilizando o hash do arquivo
            instance.determine_mime_type()
            instance.determine_file_size()
            instance._save_in_signal = True
            instance.save()
        finally:
            del instance._save_in_signal
