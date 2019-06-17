from xram_memory.artifact.models import Newspaper
from xram_memory.lib import NewsFetcher
from django import forms


class NewspaperAdminForm(forms.ModelForm):
    set_basic_info = forms.BooleanField(
        label="Tentar inferir informações sobre este site automaticamente",
        required=False,
        help_text="Apenas com o endereço do site preenchido, o sistema preencherá os outros campos automaticamente",
    )
    fetch_logo = forms.BooleanField(
        label="Tentar adicionar um logotipo para este site",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """
        Define e altera a descrição de campos customizados para indicar operações adicionais sobre
        o modelo
        """
        super().__init__(*args, **kwargs)

        # defina os valores para os campos acima de acordo com o estado do modelo
        self.initial['set_basic_info'] = not self.instance.has_basic_info
        self.initial['fetch_logo'] = not self.instance.has_logo

    def clean(self):
        """
        Faz validações customizadas sobre os dados informados pelo usuário
        """
        cleaned_data = super().clean()
        # operações adicionais sobre o modelo

        set_basic_info = cleaned_data.get(
            'set_basic_info', False)
        fetch_logo = cleaned_data.get(
            'fetch_logo', False)

        url = cleaned_data.get('url', None)
        title = cleaned_data.get('title', None)

        if not set_basic_info:
            if not title:
                self.add_error(
                    'title', 'Se você optou por inserir os dados manualmente, é necessário informar ao menos um título')
            if not url and self.instance.pk is None:
                self.add_error(
                    'slug', 'Se você optou por inserir os dados manualmente, é necessário informar um endereço')

        # define em campos privados do modelo quais operações adicionais o método save() deve
        # realizar
        self.instance._set_basic_info = set_basic_info
        self.instance._fetch_logo = fetch_logo

        if url and set_basic_info:
            try:
                title = NewsFetcher.fetch_web_title(url)
                if not title:
                    raise ValueError()
            except ValueError:
                self.add_error(
                    'title', "Não foi possível determinar um título automaticamente, preencha ele manualmente.")
            except:
                self.add_error(None,
                               "Não foi possível determinar automaticamente informações sobre este site no momento, por-favor insira os dados dele manualmente.")

        return cleaned_data
