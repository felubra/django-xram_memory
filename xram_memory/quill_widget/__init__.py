from django.forms.widgets import Widget
from django.forms import Media
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError


def no_empty_html(value):
    """
    Um simples validador que converte html em texto para verificar se o texto não está em branco.
    """
    soup = BeautifulSoup(value)
    if not soup.get_text().strip():
        raise ValidationError('Este campo não pode ficar em branco.')


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

    def __init__(self, attrs):
        super().__init__(attrs)
        self.attrs['data-theme'] = attrs.get('data-theme', 'snow') if attrs.get(
            'data-theme', 'snow') in ['snow', 'bubble'] else 'snow'

    @property
    def media(self):
        css = {
            'screen, projection': (
                'quill/quill.{}.css'.format(self.attrs['data-theme']),
                'quill_widget/css/quill-widget.css',
            )
        }
        js = (
            'quill/quill.js',
            'quill_widget/js/quill-widget.js',
        )
        return Media(css=css, js=js)
