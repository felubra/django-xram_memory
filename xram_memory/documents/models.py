from django.db import models
from ..artifact.models import Artifact
from ..archived_news.models import ArchivedNews

# Create your models here.


class File(Artifact):
    filename = models.CharField(max_length=255)

    class Meta:
        abstract = True


class PDFFile(File):
    pass


class ArchivedNewsPDFCapture(File):
    archived_news = models.ForeignKey(
        ArchivedNews, on_delete=models.PROTECT, related_name="parent_archived_news")
