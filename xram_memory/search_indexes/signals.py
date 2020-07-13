from django_elasticsearch_dsl.signals import RealTimeSignalProcessor
from xram_memory.utils.decorators import disable_for_loaddata

class FixtureAwareSignalProcessor(RealTimeSignalProcessor):
    """
    Simples classe que desativa os sinais de RealTimeSignalProcessor no caso do carregamento
    de fixtures.
    """
    def __getattribute__(self, name):
        """
        Decore todos os métodos da classe original que comecem com 'handle_',
        pois esses são os métodos ligados aos sinais que queremos sumprimir
        a execução.
        """
        attr = super().__getattribute__(name)
        if name.startswith('handle_'):
            return disable_for_loaddata(attr)
        return attr
