from django.dispatch import receiver
from django.db.models.signals import post_save
from ..archived_news.models import ArchivedNews
from .fetcher import process_news, save_news_as_pdf
import logging
import django_rq


logger = logging.getLogger(__name__)


@receiver(post_save, sender=ArchivedNews)
def add_news_archive_to_queue(sender, **kwargs):
    try:
        archived_news = kwargs['instance']
        if not archived_news:
            return
        # Se o usuário optou por uma inserção manual, não faça o processamento automático
        if archived_news.manual_insertion:
            return
        if hasattr(archived_news, '_job_processing'):
            return

        if (archived_news.is_new or archived_news.has_error):
            try:
                # @todo verificar se o serviço de filas está funcionando (se existe conexão com o redis)
                # e logar um aviso caso contrário

                # Adicione uma flag ao objeto para evitar que esse handler execute infinitamente,
                # já que algumas das funções abaixo podem chamar o save()
                archived_news._job_processing = True

                process_news.delay(archived_news)

                save_news_as_pdf.delay(archived_news)
                # adicione a notícia na fila para  baixar
                # altere o status para 'agendado'
                # salve o modelo
            finally:
                del archived_news._job_processing
    except:
        pass
