from .users.models import User
from django.db import models

# Modelos abstratos, usados como pai para alguns modelos de outros apps


class TraceableModel(models.Model):
    created_by = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name='%(class)s_creator', null=True, editable=False)
    modified_by = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name='%(class)s_last_modifier', null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
