from xram_memory.lib.stopwords import stopwords
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, now


def PluginRegistryFor(plugin_type):
    """
    Função fábrica para geração de registros para tipos de plugins.
    Ele gera uma metaclasse que é usada para guardar os tipos de plugins implementados.
    """
    PLUGIN_TYPES = ['Archive', 'PDFCapture', 'BasicInfo']

    if plugin_type not in PLUGIN_TYPES:
        raise ValueError(
            "Tipo de plugin não suportado: {}".format(plugin_type))

    class PluginRegistry(type):
        """
        Ponto de montagem para plugins usados pelo serviço NewsFetcher.
        O objeto da classe guarda uma lista com os plugins registrados - o registro acontece na
        inicialização da própria classe do plugin.
        """
        def __init__(cls, name, bases, attrs):
            if not hasattr(cls, 'plugins'):
                # Esta é uma classe de registro de plugins, crie uma lista vazia.
                cls.plugins = []
            else:
                # Esta é uma classe que implementa um tipo de plugin, adicione-a na lista.
                cls.plugins.append(cls)

        def get_plugins(self):
            """
            Retorna os plugins registrados.
            Como efeito colateral, esta função também estará disponível nos plugins.
            """
            return self.plugins

    PluginRegistry.__name__ = '{}{}'.format(
        plugin_type, PluginRegistry.__name__)
    return PluginRegistry


class ArchiveNewsFetcherPlugin(metaclass=PluginRegistryFor("Archive")):
    """
    Plugins, subclasses de ArchiveNewsFetcherPlugin, devem ter os atributos abaixo:

    fetch: função estática que recebe uma url e retorna outra url para a versão arquivada da url
    passada num arquivo qualquer.
    """
    pass


class PDFCaptureNewsFetcherPlugin(metaclass=PluginRegistryFor("PDFCapture")):
    """
    Plugins, subclasses de PDFCaptureNewsFetcherPlugin, devem ter os atributos abaixo:

    get_pdf_capture: função estática que recebe uma url e retorna um ponteiro para um arquivo aberto
    com a captura em PDF já gerada em seu conteúdo. A função deve implementar um gerenciador de
    contexto, sendo que o ponteiro/arquivo deve ser retornado ao se entrar no contexto e apagado
    na saída do contexto.

    failback: determina se esse plugin será usado em último caso se nenhum outro plugin estiver
    disponível para capturar determinada url.
    """
    pass


class BasicInfoNewsFetcherPlugin(metaclass=PluginRegistryFor("BasicInfo")):
    """
    Plugins, subclasses de BasicInfoNewsFetcherPlugin, devem ter os atributos abaixo:

    get_pdf_capture: função estática que recebe uma url e retorna um ponteiro para um arquivo aberto
    com a captura em PDF já gerada em seu conteúdo. A função deve implementar um gerenciador de
    contexto, sendo que o ponteiro/arquivo deve ser retornado ao se entrar no contexto e apagado
    na saída do contexto.

    failback: determina se esse plugin será usado em último caso se nenhum outro plugin estiver
    disponível para capturar determinada url.
    """
    BASIC_EMPTY_INFO = {'title': '', 'authors': '', 'body': '', 'teaser': '',
                        'published_date': '', 'language': '', 'image': '', 'keywords': []}

    @classmethod
    def clean(self, info_dict):
        keywords_for_language = stopwords.get(info_dict["language"], [])
        if len(keywords_for_language) > 0:
            info_dict["keywords"] = [
                keyword for keyword in info_dict["keywords"] if keyword not in keywords_for_language]

        # Se a data de publicação veio como string, tente transformá-la num objeto datetime
        if isinstance(info_dict['published_date'], str):
            try:
                info_dict['published_date'] = parse_datetime(
                    info_dict['published_date'])
            except ValueError:
                info_dict['published_date'] = None
        # Se a data de publicação não tem informações de fuso-horário, transforme-a para o fuso local
        if (info_dict['published_date'] and not info_dict['published_date'].tzinfo):
            info_dict['published_date'] = make_aware(
                info_dict['published_date'])
        return info_dict
