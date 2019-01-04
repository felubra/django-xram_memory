import logging
import django_rq
import redis

from django.dispatch import receiver
from django.db.models.signals import post_save

from ..archived_news.models import ArchivedNews
from .fetcher import process_news, save_news_as_pdf, verify_if_in_archive_org


logger = logging.getLogger(__name__)


@receiver(post_save, sender=ArchivedNews)
def add_news_archive_to_queue(sender, **kwargs):
    try:
        archived_news: ArchivedNews = kwargs['instance']
        if not archived_news:
            return

        if hasattr(archived_news, '_job_processing'):
            return

        if archived_news.needs_reprocessing:
            try:
                # Adicione uma flag ao objeto para evitar que esse handler execute infinitamente,
                # já que algumas das funções abaixo podem chamar o save()
                archived_news._job_processing = True

                if archived_news.force_basic_processing:
                    process_news.delay(archived_news)

                if archived_news.force_archive_org_processing:
                    verify_if_in_archive_org.delay(archived_news)

                if archived_news.force_pdf_capture:
                    save_news_as_pdf.delay(archived_news)

                # @todo configurar o django_rq para reutilizar a conexão do cache do redis-cache
                # verifique se o serviço de filas está funcionando (se existe conexão com o redis)
                fq = django_rq.queues.get_failed_queue()
                if fq.count > 0:
                    logger.warn(
                        "Existem {} trabalhos que falharam na fila.".format(fq.count))
            except redis.exceptions.ConnectionError as e:
                logger.error(
                    "Não foi possível processar os trabalhos da fila para a notícia {}, porque o servidor do Redis não está disponível no momento: {}".format(
                        archived_news.pk, e)
                )
                archived_news.status = ArchivedNews.STATUS_ERROR_NO_QUEUE
                archived_news.save()
            finally:
                del archived_news._job_processing
    except:
        pass
