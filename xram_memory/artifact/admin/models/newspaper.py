from xram_memory.artifact.tasks import newspaper_set_logo_from_favicon
from xram_memory.artifact.models import Newspaper
from xram_memory.utils import celery_is_avaliable
from ..forms.newspaper import NewspaperAdminForm
from django.contrib import messages
from django.contrib import admin


def schedule_for_logo_acquisition(modeladmin, request, queryset):
    if celery_is_avaliable():
        # TODO: agrupar e separar em pedaços
        for newspaper in queryset:
            newspaper_set_logo_from_favicon.s(newspaper.pk).apply_async()
        modeladmin.message_user(
            request,
            "{} site(s) foi(ram) adicionado(s) à fila para captura de logotipo".format(
                len(queryset)
            ),
            messages.INFO,
        )
    else:
        modeladmin.message_user(
            request,
            "Não é possível usar esta funcionalidade no momento, porque o servidor de filas não está disponível. Se o erro persistir, contate o administrador.",
            messages.ERROR,
        )


schedule_for_logo_acquisition.short_description = (
    "Buscar logotipos para sites selecionados"
)


def remove_logos(modeladmin, request, queryset):
    for newspaper in queryset:
        if getattr(newspaper, "logo", None) and getattr(newspaper.logo, "file", None):
            newspaper.logo.delete(True)


remove_logos.short_description = "Deletar logotipos"


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    form = NewspaperAdminForm
    list_display = (
        "id",
        "title",
        "created_by",
        "modified_by",
        "created_at",
        "modified_at",
        "url",
        "logo",
    )
    list_filter = (
        "created_at",
        "modified_at",
    )
    list_display_links = ("title",)
    date_hierarchy = "created_at"
    actions = [schedule_for_logo_acquisition, remove_logos]
    list_select_related = (
        "created_by",
        "modified_by",
    )
