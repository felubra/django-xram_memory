PLUGIN_TYPES = ['Archive', 'PDFCapture', 'BasicInfo']


def PluginRegistryFor(plugin_type):
    """
    Função fábrica para geração de registros para tipos de plugins.
    Ele gera uma metaclasse que é usada para guardar os tipos de plugins implementados.
    """
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
    Plugins, subclasses desta, devem ter os atributos abaixo:

    fetch: função estática que recebe uma url e retorna outra url para a versão arquivada da url
    passada num arquivo qualquer.
    """
    pass


class PDFCaptureNewsFetcherPlugin(metaclass=PluginRegistryFor("PDFCapture")):
    """
    Plugins, subclasses desta, devem ter os atributos abaixo:

    get_pdf_capture: função estática que recebe uma url e retorna um ponteiro para um arquivo aberto
    com a captura em PDF já gerada em seu conteúdo. A função deve implementar um gerenciador de
    contexto, sendo que o ponteiro/arquivo deve ser retornado ao se entrar no contexto e apagado
    na saída do contexto.
    """
    pass


class BasicInfoNewsFetcherPlugin(metaclass=PluginRegistryFor("BasicInfo")):
    pass
