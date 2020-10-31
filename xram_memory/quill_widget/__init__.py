from django.forms.widgets import Widget
from django.forms import Media
import json


EDITOR_COLORS = json.dumps(["#e60000", "#ff9900", "#ffff00", "#008a00", "#0066cc",
                            "#9933ff", "#ffffff", "#facccc", "#ffebcc", "#ffffcc",
                            "#cce8cc", "#cce0f5", "#ebd6ff", "#bbbbbb", "#f06666",
                            "#ffc266", "#ffff66", "#66b966", "#66a3e0", "#c285ff",
                            "#888888", "#a10000", "#b26b00", "#b2b200", "#006100",
                            "#0047b2", "#6b24b2", "#444444", "#5c0000", "#663d00",
                            "#666600", "#003700", "#002966", "#3d1466", "#000000",
                            ])

DEFAULT_EDITOR = {
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
    'data-toolbar': '''[
                                ["bold","italic","underline","strike"],
                                [{"align":["","center","right","justify"]}],
                                [{"color":%s},{"background": %s}],["link","image"],
                                ["clean"]]''' % (EDITOR_COLORS, EDITOR_COLORS),
    'data-formats': 'bold,italic,strike,underline,align,color,background,image,link'
}


def make_editor_opt(placeholder, base_options=DEFAULT_EDITOR):
    return {**base_options, **{'placeholder': placeholder}}


class QuillWidget(Widget):
    template_name = 'quill_widget/widget.html'

    def __init__(self, attrs):
        super().__init__(attrs)
        self.attrs['data-theme'] = attrs.get('data-theme', 'snow') if attrs.get(
            'data-theme', 'snow') in ['snow', 'bubble'] else 'snow'
        self.attrs['data-formats'] = attrs.get(
            'data-formats', '["bold","italic","strike"]')
        self.attrs['data-toolbar'] = attrs.get(
            'data-toolbar', '["bold","italic","strike"]')

    @property
    def media(self):
        css = {
            'screen, projection': (
                'quill/dist/quill.core.css',
                'quill/dist/quill.{}.css'.format(self.attrs['data-theme']),
                'quill_widget/css/quill-widget.css',
            )
        }
        js = (
            'screenfull/dist/screenfull.js',
            'quill/dist/quill.js',
            'quill_widget/js/quill-widget.js',
        )
        return Media(css=css, js=js)

    def format_value(self, value):
        """
        TODO: limpar o valor para o quill.js (remover javascripts?)
        """
        value = super().format_value(value)
        if value == '' or value is None:
            return ''
        return str(value)
