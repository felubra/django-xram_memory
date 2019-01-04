from django.apps import AppConfig


class LoggerConfig(AppConfig):
    name = 'xram_memory.logger'

    def ready(self):
        from xram_memory.logger import receivers
