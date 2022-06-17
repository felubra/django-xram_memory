from django.apps import AppConfig


class ArtifactConfig(AppConfig):
    name = "xram_memory.artifact"
    verbose_name = "Artefatos do acervo"

    def ready(self):
        from xram_memory.artifact.receivers import (
            DocumentSignalProcessor,
            NewsSignalProcessor,
            NewspaperSignalProcessor,
        )

        self.signal_processors = {
            "documents": DocumentSignalProcessor(),
            "news": NewsSignalProcessor(),
            "newspaper": NewspaperSignalProcessor(),
        }
