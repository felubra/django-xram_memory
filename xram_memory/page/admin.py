from django import forms
from django.contrib import admin
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.widgets import ImageClearableFileInput
from xram_memory.base_models import TraceableEditorialAdminModel
from xram_memory.quill_widget import QuillWidget, make_editor_opt, TEASER_EDITOR_OPTIONS

from .models import StaticPage


class StaticPageAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            "body": QuillWidget(attrs=make_editor_opt("Conteúdo da página...")),
            "teaser": QuillWidget(
                attrs=make_editor_opt(
                    "Resumo ou chamada para esta página...", TEASER_EDITOR_OPTIONS
                )
            ),
        }


@admin.register(StaticPage)
class StaticPageAdmin(TraceableEditorialAdminModel):
    form = StaticPageAdminForm
    list_display = (
        "id",
        "title",
        "created_by",
        "modified_by",
        "created_at",
        "modified_at",
        "show_in_menu",
        "show_in_home",
    )
    list_filter = (
        "created_by",
        "modified_by",
        "created_at",
        "modified_at",
        "show_in_menu",
    )
    prepopulated_fields = {
        "url": ("title",),
    }

    INSERT_FIELDSETS = (
        (
            "Informações básicas",
            {
                "fields": (
                    "title",
                    "teaser",
                    "body",
                )
            },
        ),
        (
            "Informações adicionais",
            {
                "fields": (
                    "url",
                    "teaser_text",
                    "image",
                    "show_in_menu",
                    "show_in_home",
                ),
            },
        ),
    )
    list_display_links = (
        "title",
        "id",
    )
    date_hierarchy = "created_at"
    formfield_overrides = {
        ThumbnailerImageField: {"widget": ImageClearableFileInput},
    }
    list_select_related = (
        "created_by",
        "modified_by",
    )

    def get_fieldsets(self, request, obj):
        """
        Use um conjunto diferente de fieldsets para adição e edição
        """
        # TODO: colocar o fieldset das capturas de página antes do fieldset com as informações gerais
        super().get_fieldsets(request, obj)
        return self.INSERT_FIELDSETS + self.COMMON_FIELDSETS
