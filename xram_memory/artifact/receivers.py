from django.dispatch import receiver
from django.db.models.signals import post_save

from xram_memory.artifact.models import Document, News


@receiver(post_save)
def set_mimetype_filesize_for_documents(sender, **kwargs):
    """
    Defina o tamanho e o tipo do arquivo para documentos.
    """
    instance = kwargs['instance']

    if hasattr(instance, '_save_in_signal'):
        return

    if isinstance(instance, (Document)):
        try:
            # TODO: otimizar as funções abaixo com lru_cache utilizando o hash do arquivo
            instance.determine_mime_type()
            instance.determine_file_size()
            # Adicione uma flag privada no modelo para evitar que esse handler execute
            # infinitamente, já que vamos chamar o save() aqui
            instance._save_in_signal = True
            instance.save()
        finally:
            del instance._save_in_signal


@receiver(post_save, sender=News)
def index_post(sender, **kwargs):
    news = kwargs['instance']
    if not news:
        return
    # @todo: verificar porque não posso fazer o tratamento de exceção aqui

    news.indexing()
