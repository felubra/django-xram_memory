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
    pass


class PDFCaptureNewsFetcherPlugin(metaclass=PluginRegistryFor("PDFCapture")):
    pass


class BasicInfoNewsFetcherPlugin(metaclass=PluginRegistryFor("BasicInfo")):
    pass
