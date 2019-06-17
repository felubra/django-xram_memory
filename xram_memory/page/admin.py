import json

from django import forms
from django.contrib import admin
from xram_memory.base_models import TraceableEditorialAdminModel
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerImageField
from xram_memory.quill_widget import QuillWidget

from .models import StaticPage


class StaticPageAdminForm(forms.ModelForm):
    class Meta:
        EDITOR_COLORS = json.dumps(["#e60000", "#ff9900", "#ffff00", "#008a00", "#0066cc",
                                    "#9933ff", "#ffffff", "#facccc", "#ffebcc", "#ffffcc",
                                    "#cce8cc", "#cce0f5", "#ebd6ff", "#bbbbbb", "#f06666",
                                    "#ffc266", "#ffff66", "#66b966", "#66a3e0", "#c285ff",
                                    "#888888", "#a10000", "#b26b00", "#b2b200", "#006100",
                                    "#0047b2", "#6b24b2", "#444444", "#5c0000", "#663d00",
                                    "#666600", "#003700", "#002966", "#3d1466", "#000000",
                                    ])

        BODY_EDITOR_OPTIONS = {
            'placeholder': 'Conteúdo da página...',
            'data-toolbar': '''[
                                [{"header":[2,3,4,5,6,false]}],
                                ["bold","italic","underline","strike"],
                                [{"align":["","center","right","justify"]}],
                                [{"color":%s},{"background": %s},"blockquote"],
                                ["link","image"],[{"list":"bullet"},{"list":"ordered"}],
                                ["clean"]]''' % (EDITOR_COLORS, EDITOR_COLORS),
            'data-formats': '''header,bold,italic,strike,underline,align,color,
                                                background,blockquote,link,list,image'''
        }

        TEASER_EDITOR_OPTIONS = {
            'placeholder': 'Resumo ou chamada para esta página...',
            'data-toolbar': '''[
                                ["bold","italic","underline","strike"],
                                [{"align":["","center","right","justify"]}],
                                [{"color":%s},{"background": %s}],["link","image"],
                                ["clean"]]''' % (EDITOR_COLORS, EDITOR_COLORS),
            'data-formats': 'bold,italic,strike,underline,align,color,background,image,link'
        }

        widgets = {
            'body': QuillWidget(attrs=BODY_EDITOR_OPTIONS),
            'teaser': QuillWidget(attrs=TEASER_EDITOR_OPTIONS),
        }


@admin.register(StaticPage)
class StaticPageAdmin(TraceableEditorialAdminModel):
    form = StaticPageAdminForm
    list_display = (
        'id',
        'title',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'show_in_menu',
    )
    list_filter = (
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
        'show_in_menu',
    )
    prepopulated_fields = {'url': ('title', ), }

    INSERT_FIELDSETS = (
        ('Informações básicas', {
            'fields': ('title', 'teaser', 'body',)
        }),

        ('Informações adicionais', {
            'fields': ('url', 'teaser_text', 'image', 'show_in_menu',),
        }),
    )
    list_display_links = ('title', 'id',)
    date_hierarchy = 'created_at'
    formfield_overrides = {
        ThumbnailerImageField: {'widget': ImageClearableFileInput},
    }
    list_select_related = (
        'created_by',
        'modified_by',
    )

    def get_fieldsets(self, request, obj):
        """
        Use um conjunto diferente de fieldsets para adição e edição
        """
        # TODO: colocar o fieldset das capturas de página antes do fieldset com as informações gerais
        super().get_fieldsets(request, obj)
        return self.INSERT_FIELDSETS + self.COMMON_FIELDSETS
