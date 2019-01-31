from django.forms.widgets import Widget
from django.forms import Media


class QuillWidget(Widget):
    template_name = 'quill_widget/widget.html'

    def format_value(self, value):
        """
        TODO: limpar o valor para o quill.js (remover javascripts?)
        """
        value = super().format_value(value)
        if value == '' or value is None:
            return ''
        return str(value)

    @property
    def media(self):
        css = {
            'screen, projection': (
                'quill/quill.snow.css',
                'quill_widget/css/quill-widget.css',
            )
        }
        js = (
            'quill/quill.js',
            'quill_widget/js/quill-widget.js',
        )
        return Media(css=css, js=js)
