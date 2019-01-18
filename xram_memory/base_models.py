from django.contrib import admin
from django.db import models

from .users.models import User
# Modelos abstratos, usados como pai para alguns modelos de outros apps


class TraceableModel(models.Model):
    created_by = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name='%(class)s_creator', null=True, editable=False, verbose_name="Criado por")
    modified_by = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name='%(class)s_last_modifier', null=True, editable=False, verbose_name="Modificado por")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em")
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name="Modificado em")

    class Meta:
        abstract = True


class TraceableEditorialModel(TraceableModel):
    '''
    Modelo que implementa um fluxo editorial básico
    '''
    published = models.BooleanField(verbose_name="Publicado?", default=True)
    featured = models.BooleanField(
        verbose_name="Em destaque na página inicial?", default=True)

    class Meta:
        abstract = True


class TraceableAdminModel(admin.ModelAdmin):
    fieldsets = (('Informações gerais', {
        'fields': ('created_by', 'modified_by',
                   'created_at', 'modified_at')
    }),)
    readonly_fields = ('created_by', 'modified_by',
                       'created_at', 'modified_at')

    def save_model(self, request, obj, form, change):
        if not change:
            # adicione um usuário criador, quando estivermos criando
            obj.created_by = request.user
        # em todas situações, adicione um usuário modificador
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        abstract = True
