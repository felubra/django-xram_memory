from xram_memory.lib.news_fetcher.plugins.base import (
    ArchivePluginBase, PDFCapturePluginBase, BasicInfoPluginBase)
from django.utils.timezone import make_aware, now
from xram_memory.artifact import models
from contextlib import contextmanager
from random import choice
from pathlib import Path
import datetime
import factory
import pytest
import os

NEWS_INFO_MOCK = {'authors': 'Ana Carolina Cortez,Eraldo Peres',
                  'body': 'Embora apenas 55,6 bilhões de reais sejam considerados "pedaladas" oficialmente, o Governo decidiu se antecipar e abafar questionamentos futuros do TCU porque o órgão já estava investigando se o esquema das pedaladas também se repetiu este ano —ou seja, já no atual mandato da presidenta— e esse era um dos argumentos da oposição para dizer que ela teria cometido crime de responsabilidade.\n\n"Daqui para frente, todos os pagamentos seguirão o sistema de 2015: serão feitos tempestivamente", esclareceu Otávio Ladeira, secretário-interino do Tesouro. Ladeira não quis emitir opinião a respeito das consequências políticas do pagamento das pedaladas. Questionado se o pagamento das dívidas enfraquecia o argumento do impeachment da Dilma, o secretário limitou-se a dizer que "não cabe ao Tesouro se posicionar sobre qualquer análise em torno do tema".\n\nSe depender do presidente da Câmara, Eduardo Cunha, não haverá trégua para Dilma. Segundo ele, o pagamento das pedaladas não invalida o pedido de impeachment que está em tramitação na Casa. Em café da manhã com jornalistas na última terça-feira (29), Cunha se antecipou ao movimento e afirmou que o processo de impeachment não se baseia nas contas de 2014, mas em manobras que teriam sido praticadas em 2015, como a emissão de decretos presidenciais para abertura de créditos extras sem o aval do Congresso. A denúncia faz parte de uma investigação que corre no Ministério Público de Contas e ainda não há um parecer oficial a respeito, nem previsão de quando ele será divulgado. Além disso, Cunha também se prepara para recorrer da decisão do Supremo Tribunal Federal (STF) que devolveu o impeachment à estaca zero na Câmara, um imbróglio que só começará a ser resolvido em fevereiro.\n\nMas de onde o Governo vai tirar dinheiro?\n\nPara quitar os 72,4 bilhões de reais das pedaladas e ganhar, pelo menos, uma trégua nessa discussão, o Governo retirou ao longo de 2015 recursos da "Conta Única do Tesouro", uma espécie de "poupança" alimentada por excesso de arrecadação de anos anteriores, criada em 1986, que serve como colchão de liquidez na administração da dívida pública.\n\nAinda que o Governo minimize um imbróglio contábil e político com o pagamento das pedaladas, a operação terá impactos sobre o nível de endividamento do Governo, que já está elevado - o que ajuda a explicar o porquê desse dinheiro nunca ter sido utilizado para evitar que as pedaladas acontecessem. Atualmente, a dívida bruta do país equivale a 65,1% do Produto Interno Bruto (PIB) e, com as pedaladas, se aproximará muito do nível considerado alarmante pelo mercado, de 70%. A dívida pública sobe porque essa injeção de recursos da "Conta Única" na economia tende a elevar mais a inflação. Para conter esse efeito colateral, o Governo acaba vendendo títulos para enxugar o dinheiro extra em circulação. Desta forma, aumenta seu nível de endividamento.\n\nMesmo pagando as pedaladas da primeira gestão, Dilma ainda mantém uma incômoda pedra no sapato para 2016. Logo no primeiro trimestre, deve sair o resultado das investigações do Ministério Público de Contas em torno das suspeitas de pedaladas em 2015. A confissão de culpa já foi feita pelo Governo no âmbito das pedaladas —afinal, ele chegou a pagar dívidas do primeiro semestre deste ano com os bancos. Mas ainda falta esclarecer a emissão de decretos presidenciais, no valor de 2,5 bilhões de reais, para gerar recursos extras, sem aprovação no Congresso. Esse é o argumento no qual Cunha deve investir desta vez, já que o mote das pedaladas foi bastante enfraquecido nesta quarta.',
                  'image': 'https://ep00.epimg.net/brasil/imagenes/2015/12/29/economia/1451418696_403408_1451421222_noticia_normal.jpg',
                  'keywords': ['pedaladas', 'dilma', 'governo', 'enfraquecer', 'argumento', 'impeachment', 'paga', '2015', 'Eduardo Cunha', 'Governo', '30 DEZ 2015 - 21:22 CET', 'Política', 'Presidência Brasil', 'Corrupção', 'Nelson Barbosa', 'Administração Estado', 'Financiamento ilegal', 'Impeachment', 'Ministério Fazenda', 'Governo Brasil', 'Economia', 'CRISE BRASILEIRA', 'Ministérios', 'Índice', 'Atividade legislativa', 'Conflitos políticos', 'Administração pública', 'Presidente Brasil', 'Impeachment Dilma Rousseff'],
                  'language': 'pt',
                  'published_date': make_aware(datetime.datetime(2015, 12, 29, 0, 0)),
                  'teaser': 'Ladeira não quis em...a quarta.',
                  'title': 'Ladeira não quis emitir opinião a respeito das consequências políticas do pagamento das pedaladas.\nSegundo ele, o pagamento das pedaladas não invalida o pedido de impeachment que está em tramitação na Casa.\nMesmo pagando as pedaladas da primeira gestão, Dilma ainda mantém uma incômoda pedra no sapato para 2016.\nLogo no primeiro trimestre, deve sair o resultado das investigações do Ministério Público de Contas em torno das suspeitas de pedaladas em 2015.\nEsse é o argumento no qual Cunha deve investir desta vez, já que o mote das pedaladas foi bastante enfraquecido nesta quarta.'}
NEWS_ITEMS = [
    {'title': 'Granny wins World Wrestling Championship',
     'authors': 'ROY MCROYSTON',
     'body': 'Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal. She walked away with her million dollar share of the prize money, runner up Tommy Thompson from Nigeria taking half a million, and third place New Zealander John Smith receiving a warm handshake from the umpire. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip". The injection of a new wrestling style into the tournament was welcomed by spectators and Johnson’s pre- and post-match breakdances have proved entertaining to fans. However, she was still not expected to win in round three last Wednesday, facing off against title-holder Paulo "SpineSnapper" Lutti, of Vatican City. Underdog Johnson was soon showing her worth with stamina and agility easily matching last year’s winner. Lutti’s experience paid off initially as he took the first two rounds, but as Johnson became more confident her superior strength came to the fore and she clawed back two rounds to take the contest into a decider. By this time Lutti’s body language indicated that he already felt overawed by the 18 MAY 2019 2 pretender to his crown, and the newcomer took advantage of this to engage a mutual headlock which she held for three hours until the Vatican man retired from exhaustion. The next seven matches were barely a contest as the news of Johnson’s supremacy overawed all her opponents who became too indimidated to fight properly. Nigerian Tommy Thompson is also a relative newcomer to the wrestling scene, but with his 210lb frame he was expected to fare well against Johnson who weighs in at only 90lb. However Johnson’s lithe and slender, some would say scrawny, figure belies her agility and strength which she demonstrated by holding Thompson above her head several times during the bout and throwing him into the crowd once. With the scores tied at 2-2 time ran out and the contest went to a panel of judges to be assessed. They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. The new champion explained her success as the result of a strict training regimen instituted by her coach and grandson five-year-old Sammy Johnson. "I’ve been drinking ten raw eggs for breakfast every morning, sprinting fifty miles a day and carrying my daughter’s car to the end of the road and back whenever I felt my arthritis was OK" she said. Sammy added "I always knew she could do it. She’s my grandma.". The youngster is also her manager and has reportedly arranged sponsorship deals which will dwarf her one million dollar prize fund. Her new contract with headband designer Nike alone is set to earn her fourteen billion dollars over the next year. She will also be promoting Tupperware, Halliburton, the Republic of Macedonia, and Gala Bingo. Her continued participation in the sport is not assured as she wants to spend more time on her bungeejumping business, and knitting. Everyone here at the World Championships, however, hopes for her return.',
     'teaser': 'Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal',
     'published_date': now(),
     'language': 'en',
     'image': 'http://uma.via.com/imagem.jpg',
     'keywords': ['granny', 'game', 'wrestling']},
    {'title': 'Oldest woman won the World Wrestling Championship',
     'authors': 'Jian Briean',
     'body': 'The new champion explained her success as the result of a strict training regimen instituted by her coach and grandson five-year-old Sammy Johnson. "I’ve been drinking ten raw eggs for breakfast every morning, sprinting fifty miles a day and carrying my daughter’s car to the end of the road and back whenever I felt my arthritis was OK" she said. Sammy added "I always knew she could do it. She’s my grandma.". The youngster is also her manager and has reportedly arranged sponsorship deals which will dwarf her one million dollar prize fund. Her new contract with headband designer Nike alone is set to earn her fourteen billion dollars over the next year. She will also be promoting Tupperware, Halliburton, the Republic of Macedonia, and Gala Bingo. Her continued participation in the sport is not assured as she wants to spend more time on her bungeejumping business, and knitting. Everyone here at the World Championships, however, hopes for her return. Nigerian Tommy Thompson is also a relative newcomer to the wrestling scene, but with his 210lb frame he was expected to fare well against Johnson who weighs in at only 90lb. However Johnson’s lithe and slender, some would say scrawny, figure belies her agility and strength which she demonstrated by holding Thompson above her head several times during the bout and throwing him into the crowd once. With the scores tied at 2-2 time ran out and the contest went to a panel of judges to be assessed. They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip". The injection of a new wrestling style into the tournament was welcomed by spectators and Johnson’s pre- and post-match breakdances have proved entertaining to fans. However, she was still not expected to win in round three last Wednesday, facing off against title-holder Paulo "SpineSnapper" Lutti, of Vatican City. Underdog Johnson was soon showing her worth with stamina and agility easily matching last year’s winner. Lutti’s experience paid off initially as he took the first two rounds, but as Johnson became more confident her superior strength came to the fore and she clawed back two rounds to take the contest into a decider. By this time Lutti’s body language indicated that he already felt overawed by the pretender to his crown, and the newcomer took advantage of this to engage a mutual headlock which she held for three hours until the Vatican man retired from exhaustion. The next seven matches were barely a contest as the news of Johnson’s supremacy overawed all her opponents who became too indimidated to fight properly. Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal. She walked away with her million dollar share of the prize money, runner up Tommy Thompson from Nigeria taking half a million, and third place New Zealander John Smith receiving a warm handshake from the umpire. ',
     'teaser': 'They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip".',
     'published_date': now(),
     'language': 'en',
     'image': 'http://won.via.com/imagem2.jpg',
     'keywords': ['woman', 'old', 'fight']}
]

VALID_NEWS_URL = "https://politica.estadao.com.br/blogs/fausto-macedo/justica-decreta-bloqueio-de-r-5-bilhoes/"


class NewspaperFactory(factory.Factory):
    class Meta:
        model = models.Newspaper
    title = 'El Pais'
    url = 'https://brasil.elpais.com'
    description = "Jornal El Pais"
    logo = None


class NewsOnlyURL(factory.Factory):
    class Meta:
        model = models.News
    url = "https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html"


@contextmanager
def mocked_news_add_fetched_image(url):
    with open(str(Path(os.path.dirname(__file__), 'image.jpg')), 'rb') as f:
        yield f


@contextmanager
def mocked_news_get_pdf_capture(url):
    with open(str(Path(os.path.dirname(__file__), 'pdf.pdf')), 'rb') as f:
        yield f


def mocked_news_fetch_archived_url(url):
    return 'abacate'


class FunctionalPlugin(type):
    @staticmethod
    def fetch(url):
        return 'OK'

    @staticmethod
    def matches(url):
        return True

    @staticmethod
    @contextmanager
    def get_pdf_capture(url):
        yield 'OK'

    @staticmethod
    def parse(url, html=None):
        return choice((NEWS_ITEMS[0], NEWS_ITEMS[1],))


class NonFunctionalPlugin(type):
    @staticmethod
    def fetch(url):
        raise RuntimeError

    @staticmethod
    @contextmanager
    def get_pdf_capture(url):
        raise RuntimeError

    @staticmethod
    def parse(url, html=None):
        raise RuntimeError


class BlankPlugin(type):
    @staticmethod
    def fetch(url):
        return ''

    @staticmethod
    def parse(url, html=None):
        return BasicInfoPluginBase.BASIC_EMPTY_INFO


@pytest.fixture
def news_fetcher_plugin_factory():
    def _plugin_factory(plugins_to_build=[FunctionalPlugin, FunctionalPlugin, FunctionalPlugin]):
        plugins = []
        for plugin_no, plugin_type in enumerate(plugins_to_build):
            class Plugin(metaclass=plugin_type):
                pass
            Plugin.__name__ = 'Plugin{}'.format(plugin_no)
            plugins.append(Plugin)
        return plugins
    return _plugin_factory
