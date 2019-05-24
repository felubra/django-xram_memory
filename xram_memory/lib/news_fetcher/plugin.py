def registry(plugin_type, default_plugin=None):
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
                if default_plugin:
                    # Se este registro usa um plugin padrão, registre-o.
                    cls.plugins = [default_plugin]
                else:
                    cls.plugins = []
            else:
                # Esta é uma classe que implementa um tipo de plugin, adicione-a no registro.
                if default_plugin:
                    # Se este registro usa um plugin padrão, deixe-o sempre como última alternativa
                    # e não adicione novamente o plugin padrão.
                    if cls is not default_plugin:
                        cls.plugins.insert(-1, cls)
                else:
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
