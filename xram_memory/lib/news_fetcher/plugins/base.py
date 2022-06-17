from django.utils.timezone import make_aware
import xram_memory.lib.news_fetcher.plugin as plugin
from django.utils.dateparse import parse_datetime
from xram_memory.lib.stopwords import stopwords
from .defaults import DefaultPDFCapture
import re


class ArchivePluginBase(metaclass=plugin.registry("Archive")):
    """
    Plugins, subclasses de ArchivePluginBase, devem ter os atributos abaixo:

    fetch: função estática que recebe uma url e retorna outra url para a versão arquivada da url
    passada num arquivo qualquer.
    """

    pass


class PDFCapturePluginBase(
    metaclass=plugin.registry("PDFCapture", default_plugin=DefaultPDFCapture)
):
    """
    Plugins, subclasses de PDFCapturePluginBase, devem ter os atributos abaixo:

    get_pdf_capture: função estática que recebe uma url e retorna um ponteiro para um arquivo aberto
    com a captura em PDF já gerada em seu conteúdo. A função deve implementar um gerenciador de
    contexto, sendo que o ponteiro/arquivo deve ser retornado ao se entrar no contexto e apagado
    na saída do contexto.
    """

    pass


class BasicInfoPluginBase(metaclass=plugin.registry("BasicInfo")):
    """
    Plugins, subclasses de BasicInfoPluginBase, devem ter os atributos abaixo:

    get_pdf_capture: função estática que recebe uma url e retorna um ponteiro para um arquivo aberto
    com a captura em PDF já gerada em seu conteúdo. A função deve implementar um gerenciador de
    contexto, sendo que o ponteiro/arquivo deve ser retornado ao se entrar no contexto e apagado
    na saída do contexto.
    """

    BASIC_EMPTY_INFO = {
        "title": "",
        "authors": "",
        "body": "",
        "teaser": "",
        "published_date": None,
        "language": "",
        "image": "",
        "keywords": [],
        "subjects": [],
    }
    KEYWORDS_REGEX = r"^[\w\d_.\-]+$"
    SUBJECTS_REGEX = r"^\w.+\s.+$"

    @classmethod
    def extract_taxonomy(self, value, pattern=KEYWORDS_REGEX):
        return list(filter(lambda word: re.match(pattern, word), value))

    @classmethod
    def clean(self, info_dict):
        keywords_for_language = stopwords.get(info_dict["language"], [])
        if len(keywords_for_language) > 0:
            info_dict["keywords"] = [
                keyword
                for keyword in info_dict["keywords"]
                if keyword not in keywords_for_language
            ]
        try:
            if info_dict["published_date"]:
                try:
                    # Tente transformar strings de data em objetos datetime
                    info_dict["published_date"] = parse_datetime(
                        info_dict["published_date"]
                    )
                except TypeError:
                    # Pode ser que info_dict['published_date'] já seja uma data, ignore.
                    pass
            info_dict["published_date"] = make_aware(
                info_dict["published_date"], is_dst=False
            )
        except ValueError:
            # A data já tem informações sobre o timezone, ignore.
            pass
        except AttributeError:
            # Data inválida, defina a data como nula.
            info_dict["published_date"] = None

        return info_dict
