from django.forms.widgets import Widget


class QuillWidget(Widget):
    template_name = 'quill_widget/widget.html'

    def format_value(self, value):
        """
        TODO: limpar o valor para o quill.js (remover javascripts?)
        """
        value = super().format_value(value)
        return str(value)
