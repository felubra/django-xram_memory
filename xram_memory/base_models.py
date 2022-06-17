from django.contrib import admin
from django.db import models

from .users.models import User

# Modelos abstratos, usados como pai para alguns modelos de outros apps


class TraceableModel(models.Model):
    """
    Um modelo abstrato com informações de criação
    """

    created_by = models.ForeignKey(
        verbose_name="Criado por",
        to=User,
        on_delete=models.PROTECT,
        related_name="%(class)s_creator",
        null=True,
        editable=False,
    )
    modified_by = models.ForeignKey(
        verbose_name="Modificado por",
        to=User,
        on_delete=models.PROTECT,
        related_name="%(class)s_last_modifier",
        null=True,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name="Modificado em",
        auto_now=True,
    )

    class Meta:
        abstract = True


class TraceableEditorialModel(TraceableModel):
    """
    Modelo que implementa um fluxo editorial básico
    """

    published = models.BooleanField(
        verbose_name="Publicado?",
        default=True,
    )
    featured = models.BooleanField(
        verbose_name="Em destaque na página inicial?",
        default=True,
    )

    class Meta:
        abstract = True


class TraceableAdminModel(admin.ModelAdmin):
    """
    Modelo abstrato de administração para o preenchimento de campos de usuário.
    """

    readonly_fields = ("created_by", "modified_by", "created_at", "modified_at")

    def save_model(self, request, obj, form, change):
        """
        Preenche campos com o usuário que fez as alterações.
        """
        if not change:
            # adicione um usuário criador, quando estivermos criando
            obj.created_by = request.user
        # em todas situações, adicione um usuário modificador
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        abstract = True


class TraceableEditorialAdminModel(TraceableAdminModel):
    COMMON_FIELDSETS = (
        (
            "Informações editoriais",
            {
                "fields": (
                    ("published", "featured"),
                    "created_by",
                    "modified_by",
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )
    pass
