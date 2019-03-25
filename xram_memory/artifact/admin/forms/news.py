from django import forms
from xram_memory.artifact.models import News
from xram_memory.artifact.news_fetcher import NewsFetcher


class NewsPDFCaptureStackedInlineForm(forms.ModelForm):
    pass


class NewsImageCaptureStackedInlineForm(forms.ModelForm):
    class Meta:
        exclude = ('original_url',)


class NewsAdminForm(forms.ModelForm):
    """
    Um formulário para editar/adicionar uma notícia
    """
    # TODO: fazer com que os campos abaixo não sejam logados em revisões de conteúdo?
    # TODO: definir os campos que este formulário aceitará: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#selecting-the-fields-to-use

    # campos para definir operações adicionais para a notícia durante e após o salvamento
    set_basic_info = forms.BooleanField(
        label="Tentar inferir informações sobre essa notícia automaticamente",
        required=False,
        help_text="Apenas com o endereço da notícia preenchido, o sistema preencherá os outros campos automaticamente",
    )
    fetch_archived_url = forms.BooleanField(
        label="Procurar uma versão arquivada dessa notícia automaticamente no Internet Archive",
        help_text="O sistema solicitará uma versão arquivada dessa notícia ao Internet Archive",
        required=False,
    )
    add_pdf_capture = forms.BooleanField(
        label="Capturar a página dessa notícia em formato PDF",
        help_text="Se marcado, o sistema fará uma captura da página dessa notícia em PDF",
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
        self.initial['fetch_archived_url'] = not self.instance.archived_news_url
        self.initial['add_pdf_capture'] = not self.instance.has_pdf_capture

        if self.instance.pk is None:
            self.fields['set_basic_info'].label = 'Obter informações sobre essa notícia automaticamente'
            self.fields['fetch_archived_url'].label = 'Procurar por uma versão arquivada dessa notícia no <a href="https://archive.org/">Internet Archive</a>'
            self.fields['add_pdf_capture'].label = 'Fazer uma captura dessa notícia em formato PDF'
        else:
            self.fields['set_basic_info'].label = 'Obter informações sobre essa notícia novamente'
            self.fields['fetch_archived_url'].label = 'Procurar novamente por uma versão arquivada dessa notícia no Internet Archive'
            self.fields['add_pdf_capture'].label = 'Adicionar uma nova captura de página dessa notícia em formato PDF'

    def clean(self):
        """
        Faz validações customizadas sobre os dados informados pelo usuário
        """
        cleaned_data = super().clean()
        # operações adicionais sobre o modelo
        title = cleaned_data.get(
            'title', None)
        set_basic_info = cleaned_data.get(
            'set_basic_info', False)
        fetch_archived_url = cleaned_data.get(
            'fetch_archived_url', False)
        add_pdf_capture = cleaned_data.get(
            'add_pdf_capture', False)

        url = cleaned_data.get('url', None)
        slug = cleaned_data.get('slug', None)

        if not set_basic_info:
            if not title:
                self.add_error(
                    'title', 'Se você optou por inserir os dados manualmente, é necessário informar ao menos um título')
            if not slug and self.instance.pk is None:
                self.add_error(
                    'slug', 'Se você optou por inserir os dados manualmente, é informar um endereço')

        # define em campos privados do modelo quais operações adicionais o método save() deve
        # realizar
        self.instance._set_basic_info = set_basic_info
        self.instance._fetch_archived_url = fetch_archived_url
        self.instance._add_pdf_capture = add_pdf_capture

        # ao inserir uma notícia apenas com a url, verifica se
        # é possível ao menos obter um título para ela (obrigatório)
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
                               "Não foi possível determinar automaticamente informações sobre esta notícia no momento, por-favor insira os dados dela manualmente.")

        return cleaned_data
