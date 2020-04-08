import xram_memory.artifact.tasks as background_tasks
from xram_memory.artifact.tasks import newspaper_set_logo_from_favicon
from xram_memory.artifact.models import Newspaper
from xram_memory.utils import celery_is_avaliable
from ..forms.newspaper import NewspaperAdminForm
from django.contrib import messages
from django.contrib import admin
from celery import group
from django.db import transaction


def schedule_for_logo_acquisition(modeladmin, request, queryset):
    if celery_is_avaliable():
        # TODO: agrupar e separar em pedaços
        for newspaper in queryset:
            newspaper_set_logo_from_favicon.s(newspaper.pk).apply_async()
        modeladmin.message_user(
            request, '{} site(s) foi(ram) adicionado(s) à fila para captura de logotipo'.format(len(queryset)), messages.INFO)
    else:
        modeladmin.message_user(
            request, 'Não é possível usar esta funcionalidade no momento, porque o servidor de filas não está disponível. Se o erro persistir, contate o administrador.', messages.ERROR)


schedule_for_logo_acquisition.short_description = "Buscar logotipos para sites selecionados"


def remove_logos(modeladmin, request, queryset):
    for newspaper in queryset:
        if getattr(newspaper, 'logo', None) and getattr(newspaper.logo, 'file', None):
            newspaper.logo.delete(True)


remove_logos.short_description = 'Deletar logotipos'


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    form = NewspaperAdminForm
    list_display = (
        'id',
        'title',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'url',
        'logo',
    )
    list_filter = ('created_at', 'modified_at', )
    list_display_links = ('title',)
    date_hierarchy = 'created_at'
    actions = [schedule_for_logo_acquisition, remove_logos]
    list_select_related = (
        'created_by',
        'modified_by',
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        instance = form.instance

        # Executa
        execute_async = celery_is_avaliable()
        fields_and_tasks_info = [
            (getattr(instance, '_set_basic_info', False), background_tasks.newspaper_set_basic_info.s(instance.pk)),
            (getattr(instance, '_fetch_logo', False), background_tasks.newspaper_set_logo_from_favicon.s(instance.pk)),
        ]

        tasks_to_run = []
        for status, task in fields_and_tasks_info:
            if status:
                tasks_to_run.append(task)
        tasks_to_run = group(tasks_to_run)

        if execute_async:
            transaction.on_commit(lambda : tasks_to_run.apply_async())
            if len(tasks_to_run):
                self.message_user(request,
                    'As informações do site estão sendo atualizadas', messages.INFO)
        else:
            transaction.on_commit(lambda: tasks_to_run.apply())