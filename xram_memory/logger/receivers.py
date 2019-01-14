from loguru import logger
from django.dispatch import receiver

from xram_memory.archived_news.models import ArchivedNews
from xram_memory.news_fetcher import signals as process_signals


@receiver(process_signals.basic_info_started)
def basic_info_job_started(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Início do processamento automático para a Notícia com o id {}, atualizada por {} em {} e com o status {}'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display()
            )
        )
    except:
        logger.warning(
            'Início do processamento automático para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk)
        )


@receiver(process_signals.internet_archive_started)
def internet_archive_job_started(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Início do processo para tentar pegar uma versão arquivada no Internet Archive para a Notícia com o id {}, atualizada por {} em {} e com o status {}'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display()
            )
        )
    except:
        logger.warning(
            'Início do processo para tentar pegar uma versão arquivada no Internet Archive para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk)
        )


@receiver(process_signals.pdf_capture_started)
def pdf_capture_job_started(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Início do processo para a captura de página em PDF para a Notícia com o id {}, atualizada por {} em {} e com o status {}'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display()
            )
        )
    except:
        logger.warning(
            'Início do processo para a captura de página em PDF para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk)
        )


@receiver(process_signals.basic_info_acquired)
def basic_info_job_success(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Sucesso ao obter informações básicas para a Notícia com o id {}, atualizada por {} em {} e com o status "{}". A operação demorou {:.1f} segundos.'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['time_took'],
            )
        )
    except:
        logger.info(
            'Sucesso ao obter informações básicas para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk
            )
        )


@receiver(process_signals.internet_archive_acquired)
def internet_archive_job_success(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Sucesso ao obter uma versão arquivada no Internet Archive para a Notícia com o id {}, atualizada por {} em {} e com o status "{}". A operação demorou {:.1f} segundos.'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['time_took'],
            )
        )
    except:
        logger.info(
            'Sucesso ao obter uma versão arquivada no Internet Archive para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk
            )
        )


@receiver(process_signals.pdf_capture_acquired)
def pdf_capture_job_success(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.info(
            'Sucesso em fazer uma captura de página em PDF para a Notícia com o id {}, atualizada por {} em {} e com o status "{}". A operação demorou {:.1f} segundos. Foi criada uma nova captura de página em PDF com o id {}'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['time_took'], kwargs['pdf_capture'].pk
            )
        )
        """
        TODO: despachar um sinal para começar a gerar um relatório de captura em pdf.
        """
    except:
        logger.info(
            'Sucesso em fazer uma captura de página em PDF para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a notícia.'.format(
                archived_news.pk
            )
        )


@receiver(process_signals.basic_info_failed)
def basic_info_job_fail(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.error(
            'Falha ao tentar obter informações básicas para a Notícia com o id {}, atualizada por {} em {} e com o status "{}":{}.'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['error_message']
            )
        )
    except:
        logger.error(
            'Falha ao tentar obter informações básicas para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a falha.'.format(
                archived_news.pk
            )
        )


@receiver(process_signals.internet_archive_failed)
def internet_archive_job_fail(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.error(
            'Falha ao tentar obter uma versão arquivada no Internet Archive para a Notícia com o id {}, atualizada por {} em {} e com o status "{}":{}.'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['error_message']
            )
        )
    except:
        logger.error(
            'Falha ao tentar obter uma versão arquivada no Internet Archive para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a falha.'.format(
                archived_news.pk
            )
        )


@receiver(process_signals.pdf_capture_failed)
def pdf_capture_job_fail(sender, **kwargs):
    archived_news: ArchivedNews = kwargs['archived_news']
    if not archived_news:
        return

    try:
        logger.error(
            'Falha ao tentar capturar a página em PDF para a Notícia com o id {}, atualizada por {} em {} e com o status "{}":{}.'.format(
                archived_news.pk, archived_news.modified_by.username, archived_news.modified_at, archived_news.get_status_display(),
                kwargs['error_message']
            )
        )
    except:
        logger.error(
            'Falha ao tentar capturar a página em PDF para a Notícia com o id {}. Um erro impede que o sistema informe mais detalhes sobre a falha.'.format(
                archived_news.pk
            )
        )
