from django.db import models
from ..base_models import TraceableModel
from ..artifact.models import Artifact

# Create your models here.


class Collection(TraceableModel):
    items = models.ManyToManyField(Artifact)
    text = models.TextField()
