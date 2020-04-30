from xram_memory.artifact.models import Document, News, Newspaper
from xram_memory.taxonomy.models import Keyword, Subject
from django.db.models.signals import post_save, post_delete, m2m_changed
from .tasks import lunr_index_rebuild
from xram_memory.utils import celery_is_avaliable


def schedule_lunr_index_rebuild(sender, instance, **kwargs):
    if celery_is_avaliable():
        lunr_index_rebuild.apply_async()
    else:
        lunr_index_rebuild.apply()
    # FIXME: implementar failback para o caso do celery não estar disponível


for Model in [News, Newspaper, Keyword, Subject, Document]:
    post_save.connect(schedule_lunr_index_rebuild, Model)
    m2m_changed.connect(schedule_lunr_index_rebuild, Model)
    post_delete.connect(schedule_lunr_index_rebuild, Model)
