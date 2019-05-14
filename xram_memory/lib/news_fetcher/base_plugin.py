class NewsFetcherPluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class NewsFetcherPlugin(metaclass=NewsFetcherPluginMount):
    """
    Ponto de montagem para plugins usados pelo serviço NewsFetcher.
    Plugins que implementam essa class precisam prover os seguintes atributos:
    ========  ========================================================
    type      O tipo do plugin. Pode ser:
                'archive': plugin que busca uma versão arquivada
                para uma url em determinado serviço de arquivamento.
                'pdf_capture': um plugin especializado na geração de
                captura em pdf de uma determinada url, de acordo com
                um determinado padrão de url
                'basic_info': um plugin cujo trabalho se resume em
                retornar informações sobre determinada notícia, com
                base em sua url
    ========  ========================================================
    """
    @classmethod
    def get_archive_plugins(cls):
        return [p for p in cls.plugins if p.plugin_type == "archive"]

    @classmethod
    def get_pdf_capture_plugins(cls):
        return [p for p in cls.plugins if p.plugin_type == "pdf_capture"]

    @classmethod
    def get_basic_info_plugins(cls):
        return [p for p in cls.plugins if p.plugin_type == "basic_info"]
