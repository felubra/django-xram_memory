from xram_memory.lib.news_fetcher.plugins.base import (
    ArchivePluginBase, PDFCapturePluginBase, BasicInfoPluginBase)
from xram_memory.lib.news_fetcher import NewsFetcher
from django.core.exceptions import ValidationError
from contextlib import contextmanager
from django.utils.timezone import now
from django.test import TestCase
from random import choice

VALID_NEWS_1 = {'title': 'Granny wins World Wrestling Championship',
                'authors': 'ROY MCROYSTON',
                'body': 'Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal. She walked away with her million dollar share of the prize money, runner up Tommy Thompson from Nigeria taking half a million, and third place New Zealander John Smith receiving a warm handshake from the umpire. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip". The injection of a new wrestling style into the tournament was welcomed by spectators and Johnson’s pre- and post-match breakdances have proved entertaining to fans. However, she was still not expected to win in round three last Wednesday, facing off against title-holder Paulo "SpineSnapper" Lutti, of Vatican City. Underdog Johnson was soon showing her worth with stamina and agility easily matching last year’s winner. Lutti’s experience paid off initially as he took the first two rounds, but as Johnson became more confident her superior strength came to the fore and she clawed back two rounds to take the contest into a decider. By this time Lutti’s body language indicated that he already felt overawed by the 18 MAY 2019 2 pretender to his crown, and the newcomer took advantage of this to engage a mutual headlock which she held for three hours until the Vatican man retired from exhaustion. The next seven matches were barely a contest as the news of Johnson’s supremacy overawed all her opponents who became too indimidated to fight properly. Nigerian Tommy Thompson is also a relative newcomer to the wrestling scene, but with his 210lb frame he was expected to fare well against Johnson who weighs in at only 90lb. However Johnson’s lithe and slender, some would say scrawny, figure belies her agility and strength which she demonstrated by holding Thompson above her head several times during the bout and throwing him into the crowd once. With the scores tied at 2-2 time ran out and the contest went to a panel of judges to be assessed. They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. The new champion explained her success as the result of a strict training regimen instituted by her coach and grandson five-year-old Sammy Johnson. "I’ve been drinking ten raw eggs for breakfast every morning, sprinting fifty miles a day and carrying my daughter’s car to the end of the road and back whenever I felt my arthritis was OK" she said. Sammy added "I always knew she could do it. She’s my grandma.". The youngster is also her manager and has reportedly arranged sponsorship deals which will dwarf her one million dollar prize fund. Her new contract with headband designer Nike alone is set to earn her fourteen billion dollars over the next year. She will also be promoting Tupperware, Halliburton, the Republic of Macedonia, and Gala Bingo. Her continued participation in the sport is not assured as she wants to spend more time on her bungeejumping business, and knitting. Everyone here at the World Championships, however, hopes for her return.',
                'teaser': 'Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal',
                'published_date': now(),
                'language': 'en',
                'image': 'http://uma.via.com/imagem.jpg',
                'keywords': ['granny', 'game', 'wrestling']}

VALID_NEWS_2 = {'title': 'Oldest woman won the World Wrestling Championship',
                'authors': 'Jian Briean',
                'body': 'The new champion explained her success as the result of a strict training regimen instituted by her coach and grandson five-year-old Sammy Johnson. "I’ve been drinking ten raw eggs for breakfast every morning, sprinting fifty miles a day and carrying my daughter’s car to the end of the road and back whenever I felt my arthritis was OK" she said. Sammy added "I always knew she could do it. She’s my grandma.". The youngster is also her manager and has reportedly arranged sponsorship deals which will dwarf her one million dollar prize fund. Her new contract with headband designer Nike alone is set to earn her fourteen billion dollars over the next year. She will also be promoting Tupperware, Halliburton, the Republic of Macedonia, and Gala Bingo. Her continued participation in the sport is not assured as she wants to spend more time on her bungeejumping business, and knitting. Everyone here at the World Championships, however, hopes for her return. Nigerian Tommy Thompson is also a relative newcomer to the wrestling scene, but with his 210lb frame he was expected to fare well against Johnson who weighs in at only 90lb. However Johnson’s lithe and slender, some would say scrawny, figure belies her agility and strength which she demonstrated by holding Thompson above her head several times during the bout and throwing him into the crowd once. With the scores tied at 2-2 time ran out and the contest went to a panel of judges to be assessed. They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip". The injection of a new wrestling style into the tournament was welcomed by spectators and Johnson’s pre- and post-match breakdances have proved entertaining to fans. However, she was still not expected to win in round three last Wednesday, facing off against title-holder Paulo "SpineSnapper" Lutti, of Vatican City. Underdog Johnson was soon showing her worth with stamina and agility easily matching last year’s winner. Lutti’s experience paid off initially as he took the first two rounds, but as Johnson became more confident her superior strength came to the fore and she clawed back two rounds to take the contest into a decider. By this time Lutti’s body language indicated that he already felt overawed by the pretender to his crown, and the newcomer took advantage of this to engage a mutual headlock which she held for three hours until the Vatican man retired from exhaustion. The next seven matches were barely a contest as the news of Johnson’s supremacy overawed all her opponents who became too indimidated to fight properly. Records were smashed in Nicaragua’s World Wrestling Championship last night as 78-year-old Maud Johnson, grandmother of five, became the first woman for fifty-six years, and the oldest competitor ever, to claim the gold medal. She walked away with her million dollar share of the prize money, runner up Tommy Thompson from Nigeria taking half a million, and third place New Zealander John Smith receiving a warm handshake from the umpire. ',
                'teaser': 'They awarded Thompson a C grade whilst Johnson received an A, becoming the first grandmother to ever win the title. Having started the tournament a rank outsider she began to impress in her second match when she took US number three Ron Ronson by surprise and subdued him in twenty seconds with her unique move that has been dubbed "Maud’s Death Grip".',
                'published_date': now(),
                'language': 'en',
                'image': 'http://won.via.com/imagem2.jpg',
                'keywords': ['woman', 'old', 'fight']}


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
        return choice((VALID_NEWS_1, VALID_NEWS_2,))


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


def plugin_factory(plugins_to_build=[FunctionalPlugin, FunctionalPlugin, FunctionalPlugin]):
    plugins = []
    for plugin_no, plugin_type in enumerate(plugins_to_build):
        class Plugin(metaclass=plugin_type):
            pass
        Plugin.__name__ = 'Plugin{}'.format(plugin_no)
        plugins.append(Plugin)
    return plugins


class NewsFetcherUnitTests(TestCase):
    FUNCTIONS_THAT_ACCEPT_URL = (NewsFetcher.fetch_archived_url, NewsFetcher.fetch_basic_info,
                                 NewsFetcher.fetch_web_title, NewsFetcher.get_pdf_capture,
                                 NewsFetcher.fetch_image, NewsFetcher.build_newspaper,)

    def setUp(self):
        self.valid_news_url = "https://politica.estadao.com.br/blogs/fausto-macedo/justica-decreta-bloqueio-de-r-5-bilhoes/"
        for function in self.FUNCTIONS_THAT_ACCEPT_URL:
            if hasattr(function, 'cache_clear'):
                function.cache_clear()

    def test_function_with_invalid_urls(self):
        for function in self.FUNCTIONS_THAT_ACCEPT_URL:
            with self.assertRaises(ValidationError) as f:
                with function('invalid_url'):
                    pass

    def test_fetch_archived_url_with_valid_url(self):
        ArchivePluginBase.plugins = plugin_factory()
        url = NewsFetcher.fetch_archived_url(self.valid_news_url)
        self.assertEqual(url, 'OK')

    def test_fetch_archived_url_with_no_plugins(self):
        ArchivePluginBase.plugins = []
        with self.assertRaises(RuntimeError) as f:
            NewsFetcher.fetch_archived_url(self.valid_news_url)
        self.assertIn('Nenhum', f.exception.args[0],)

    def test_fetch_archived_url_with_blank_plugin(self):
        ArchivePluginBase.plugins = plugin_factory([BlankPlugin])
        url = NewsFetcher.fetch_archived_url(self.valid_news_url)
        self.assertEqual(url, '')

    def test_fetch_archived_url_with_blank_plugin_failed_plugin(self):
        ArchivePluginBase.plugins = plugin_factory([
            BlankPlugin, NonFunctionalPlugin])
        with self.assertRaises(RuntimeError) as f:
            NewsFetcher.fetch_archived_url(self.valid_news_url)
        self.assertIn('plugins falharam', f.exception.args[0],)

    def test_fetch_archived_url_with_blank_failed_functional_plugin(self):
        ArchivePluginBase.plugins = plugin_factory([FunctionalPlugin,
                                                    BlankPlugin,
                                                    NonFunctionalPlugin])
        url = NewsFetcher.fetch_archived_url(self.valid_news_url)
        self.assertEqual(url, 'OK')

    ###############################
    # Testes com get_pdf_capture()#
    ###############################
    def test_get_pdf_capture_with_valid_url(self):
        PDFCapturePluginBase.plugins = plugin_factory([FunctionalPlugin])
        with NewsFetcher.get_pdf_capture(self.valid_news_url) as f:
            self.assertEqual(f, 'OK')

    def test_get_pdf_capture_with_no_plugins(self):
        PDFCapturePluginBase.plugins = []
        with self.assertRaises(RuntimeError) as f:
            with NewsFetcher.get_pdf_capture(self.valid_news_url) as f:
                pass
        self.assertIn('Nenhum', f.exception.args[0],)

    def test_get_pdf_capture_with_non_functional_plugin(self):
        PDFCapturePluginBase.plugins = plugin_factory([NonFunctionalPlugin])
        with self.assertRaises(RuntimeError) as f:
            with NewsFetcher.get_pdf_capture(self.valid_news_url) as f:
                pass
        self.assertIn('alguns plugins falharam', f.exception.args[0],)

    ################################
    # Testes com fetch_basic_info()#
    ################################
    def test_fetch_basic_info_with_valid_url(self):
        BasicInfoPluginBase.plugins = plugin_factory([FunctionalPlugin])
        url = NewsFetcher.fetch_basic_info(self.valid_news_url)
        self.assertIn(url, [VALID_NEWS_2,
                            VALID_NEWS_1, ])

    def test_fetch_basic_info_with_no_plugins(self):
        BasicInfoPluginBase.plugins = []
        with self.assertRaises(RuntimeError) as f:
            NewsFetcher.fetch_basic_info(self.valid_news_url)
        self.assertIn('Nenhum', f.exception.args[0],)

    def test_fetch_basic_info_with_blank_plugin(self):
        BasicInfoPluginBase.plugins = plugin_factory([BlankPlugin])

        with self.assertRaises(RuntimeError) as f:
            NewsFetcher.fetch_basic_info(self.valid_news_url)
        self.assertIn('nenhum plugin', f.exception.args[0],)

    def test_fetch_basic_info_with_blank_plugin_failed_plugin(self):
        BasicInfoPluginBase.plugins = plugin_factory([
            BlankPlugin, NonFunctionalPlugin])
        with self.assertRaises(RuntimeError) as f:
            NewsFetcher.fetch_basic_info(self.valid_news_url)
        self.assertIn('plugins falharam', f.exception.args[0],)

    def test_fetch_basic_info_with_blank_failed_functional_plugin(self):
        BasicInfoPluginBase.plugins = plugin_factory([FunctionalPlugin,
                                                      BlankPlugin,
                                                      NonFunctionalPlugin])
        url = NewsFetcher.fetch_basic_info(self.valid_news_url)
        self.assertIn(url, [VALID_NEWS_2,
                            VALID_NEWS_1, ])

    def test_fetch_basic_info_conservative_nature(self):
        BasicInfoPluginBase.plugins = plugin_factory([FunctionalPlugin,
                                                      NonFunctionalPlugin])
        BasicInfoPluginBase.plugins[0].parse = lambda url, html: VALID_NEWS_1
        BasicInfoPluginBase.plugins[1].parse = lambda url, html: VALID_NEWS_2
        url = NewsFetcher.fetch_basic_info(self.valid_news_url)
        for key in BasicInfoPluginBase.BASIC_EMPTY_INFO.keys():
            if key == 'keywords':
                continue
            self.assertEqual(
                url[key], VALID_NEWS_1[key])
        self.assertEqual(
            url['keywords'], VALID_NEWS_1['keywords'] + VALID_NEWS_2['keywords'])
