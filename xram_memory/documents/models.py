from django.db import models
from django.conf import settings
from os.path import basename

from ..base_models import TraceableModel
from ..archived_news.models import ArchivedNews

# Create your models here.
saved_pdf_dir = settings.NEWS_FETCHER_SAVED_DIR_PDF


class Document(TraceableModel):
    '''
    Modelo abstrato para todos os tipos de documento.
    '''
    size = models.fields.PositiveIntegerField(default=0, editable=False)
    mime_type = models.fields.CharField(
        max_length=255, blank=True, editable=False)

    class Meta:
        abstract = True


class ArchivedNewsPDFCapture(Document):
    '''
    Uma captura de página de uma notícia arquivada.
    '''
    url_of_capture = models.URLField(
        max_length=255, help_text="Endereço original da notícia que gerou essa captura",
        verbose_name="Endereço", null=True, blank=True, editable=False)
    pdf_file = models.FileField(upload_to=saved_pdf_dir,
                                verbose_name="Captura da notícia em PDF",
                                blank=True)
    archived_news = models.ForeignKey(
        ArchivedNews, on_delete=models.PROTECT, related_name="pdf_captures")

    def __str__(self):
        return basename(self.pdf_file.file.name)
