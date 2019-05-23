from django.utils.timezone import make_aware
from xram_memory.artifact import models
from contextlib import contextmanager
from pathlib import Path
import datetime
import factory
import os

NEWS_INFO_MOCK = {'authors': 'Ana Carolina Cortez,Eraldo Peres',
                  'body': 'Embora apenas 55,6 bilhões de reais sejam considerados "pedaladas" oficialmente, o Governo decidiu se antecipar e abafar questionamentos futuros do TCU porque o órgão já estava investigando se o esquema das pedaladas também se repetiu este ano —ou seja, já no atual mandato da presidenta— e esse era um dos argumentos da oposição para dizer que ela teria cometido crime de responsabilidade.\n\n"Daqui para frente, todos os pagamentos seguirão o sistema de 2015: serão feitos tempestivamente", esclareceu Otávio Ladeira, secretário-interino do Tesouro. Ladeira não quis emitir opinião a respeito das consequências políticas do pagamento das pedaladas. Questionado se o pagamento das dívidas enfraquecia o argumento do impeachment da Dilma, o secretário limitou-se a dizer que "não cabe ao Tesouro se posicionar sobre qualquer análise em torno do tema".\n\nSe depender do presidente da Câmara, Eduardo Cunha, não haverá trégua para Dilma. Segundo ele, o pagamento das pedaladas não invalida o pedido de impeachment que está em tramitação na Casa. Em café da manhã com jornalistas na última terça-feira (29), Cunha se antecipou ao movimento e afirmou que o processo de impeachment não se baseia nas contas de 2014, mas em manobras que teriam sido praticadas em 2015, como a emissão de decretos presidenciais para abertura de créditos extras sem o aval do Congresso. A denúncia faz parte de uma investigação que corre no Ministério Público de Contas e ainda não há um parecer oficial a respeito, nem previsão de quando ele será divulgado. Além disso, Cunha também se prepara para recorrer da decisão do Supremo Tribunal Federal (STF) que devolveu o impeachment à estaca zero na Câmara, um imbróglio que só começará a ser resolvido em fevereiro.\n\nMas de onde o Governo vai tirar dinheiro?\n\nPara quitar os 72,4 bilhões de reais das pedaladas e ganhar, pelo menos, uma trégua nessa discussão, o Governo retirou ao longo de 2015 recursos da "Conta Única do Tesouro", uma espécie de "poupança" alimentada por excesso de arrecadação de anos anteriores, criada em 1986, que serve como colchão de liquidez na administração da dívida pública.\n\nAinda que o Governo minimize um imbróglio contábil e político com o pagamento das pedaladas, a operação terá impactos sobre o nível de endividamento do Governo, que já está elevado - o que ajuda a explicar o porquê desse dinheiro nunca ter sido utilizado para evitar que as pedaladas acontecessem. Atualmente, a dívida bruta do país equivale a 65,1% do Produto Interno Bruto (PIB) e, com as pedaladas, se aproximará muito do nível considerado alarmante pelo mercado, de 70%. A dívida pública sobe porque essa injeção de recursos da "Conta Única" na economia tende a elevar mais a inflação. Para conter esse efeito colateral, o Governo acaba vendendo títulos para enxugar o dinheiro extra em circulação. Desta forma, aumenta seu nível de endividamento.\n\nMesmo pagando as pedaladas da primeira gestão, Dilma ainda mantém uma incômoda pedra no sapato para 2016. Logo no primeiro trimestre, deve sair o resultado das investigações do Ministério Público de Contas em torno das suspeitas de pedaladas em 2015. A confissão de culpa já foi feita pelo Governo no âmbito das pedaladas —afinal, ele chegou a pagar dívidas do primeiro semestre deste ano com os bancos. Mas ainda falta esclarecer a emissão de decretos presidenciais, no valor de 2,5 bilhões de reais, para gerar recursos extras, sem aprovação no Congresso. Esse é o argumento no qual Cunha deve investir desta vez, já que o mote das pedaladas foi bastante enfraquecido nesta quarta.',
                  'image': 'https://ep00.epimg.net/brasil/imagenes/2015/12/29/economia/1451418696_403408_1451421222_noticia_normal.jpg',
                  'keywords': ['pedaladas', 'dilma', 'governo', 'enfraquecer', 'argumento', 'impeachment', 'paga', '2015', 'Eduardo Cunha', 'Governo', '30 DEZ 2015 - 21:22 CET', 'Política', 'Presidência Brasil', 'Corrupção', 'Nelson Barbosa', 'Administração Estado', 'Financiamento ilegal', 'Impeachment', 'Ministério Fazenda', 'Governo Brasil', 'Economia', 'CRISE BRASILEIRA', 'Ministérios', 'Índice', 'Atividade legislativa', 'Conflitos políticos', 'Administração pública', 'Presidente Brasil', 'Impeachment Dilma Rousseff'],
                  'language': 'pt',
                  'published_date': make_aware(datetime.datetime(2015, 12, 29, 0, 0)),
                  'teaser': 'Ladeira não quis em...a quarta.',
                  'title': 'Ladeira não quis emitir opinião a respeito das consequências políticas do pagamento das pedaladas.\nSegundo ele, o pagamento das pedaladas não invalida o pedido de impeachment que está em tramitação na Casa.\nMesmo pagando as pedaladas da primeira gestão, Dilma ainda mantém uma incômoda pedra no sapato para 2016.\nLogo no primeiro trimestre, deve sair o resultado das investigações do Ministério Público de Contas em torno das suspeitas de pedaladas em 2015.\nEsse é o argumento no qual Cunha deve investir desta vez, já que o mote das pedaladas foi bastante enfraquecido nesta quarta.'}


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
    with open(str(Path(os.path.dirname(__file__), 'files', 'image.jpg')), 'rb') as f:
        yield f


@contextmanager
def mocked_news_get_pdf_capture(url):
    with open(str(Path(os.path.dirname(__file__), 'files', 'pdf.pdf')), 'rb') as f:
        yield f


def mocked_news_fetch_archived_url(url):
    return 'abacate'
