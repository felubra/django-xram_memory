"""
Define classes utilizadas em todo o projeto
"""
from abc import ABC, abstractmethod


class SignalProcessorBase(ABC):
    signals = []
    models = []

    @abstractmethod
    def setup(self):
        """
        Para cada modelo, conecta o agendamento do trabalho ao sinal suportado.
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        Desconecta os sinais outrora conectados.
        """
        pass

    @abstractmethod
    def handler(self, *args, **kwargs):
        """
        A função a ser executada, nunca deve ser chamado diretamente
        """
        pass


class SignalProcessor(SignalProcessorBase):
    """
    Um processador de sinais que os associa a modelos definidos e pode
    ser ligado/desligado em runtime
    """

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        """
        Para cada modelo, conecta o agendamento do trabalho ao sinal suportado.
        """
        for signal in self.signals:
            for model in self.models:
                signal.connect(self.handler, model)

    def teardown(self):
        """
        Desconecta os sinais outrora conectados.
        """
        for signal in self.signals:
            for model in self.models:
                signal.disconnect(self.handler, model)
