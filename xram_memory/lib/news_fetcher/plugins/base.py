from xram_memory.lib.stopwords import stopwords
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, now
import xram_memory.lib.news_fetcher.plugin as plugin
from .defaults import DefaultPDFCapture


class ArchivePluginBase(metaclass=plugin.registry("Archive")):
    """
    Plugins, subclasses de ArchivePluginBase, devem ter os atributos abaixo:

    fetch: função estática que recebe uma url e retorna outra url para a versão arquivada da url
    passada num arquivo qualquer.
    """
    pass


class PDFCapturePluginBase(metaclass=plugin.registry("PDFCapture", default_plugin=DefaultPDFCapture)):
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
    BASIC_EMPTY_INFO = {'title': '', 'authors': '', 'body': '', 'teaser': '',
                        'published_date': '', 'language': '', 'image': '', 'keywords': []}

    @classmethod
    def clean(self, info_dict):
        keywords_for_language = stopwords.get(info_dict["language"], [])
        if len(keywords_for_language) > 0:
            info_dict["keywords"] = [
                keyword for keyword in info_dict["keywords"] if keyword not in keywords_for_language]

        # Se a data de publicação veio como string, tente transformá-la num objeto datetime

        try:
            try:
                info_dict['published_date'] = parse_datetime(
                    info_dict['published_date'])
            except TypeError:
                pass
            info_dict['published_date'] = make_aware(
                info_dict['published_date'])
        except:
            info_dict['published_date'] = None

        return info_dict
