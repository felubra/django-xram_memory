from xram_memory.artifact.models import News
from django.test import TestCase, TransactionTestCase
from loguru import logger
import datetime

logger.remove()

# Create your tests here.

# TODO: Quando for buscar uma notícia na web, usar uma fixture, já que essa notícia pode ser retirada do ar


class NewsTestCase(TestCase):
    def test_require_url_on_save(self):
        news = News(title="Abacate")
        self.assertRaises(ValueError, news.save)

    def test_save_without_title(self):
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        news.save()
        self.assertNotEqual(news.title, '')

    def test_initial_flags_state(self):
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        for field in ['thumbnail', 'published_year', 'image_capture_indexing', 'body', 'teaser', 'published_date']:
            value = getattr(news, field)
            self.assertIsNone(value)

        for field in ['title', 'authors', ]:
            value = getattr(news, field)
            self.assertEqual(value, '')

        for field in ['has_basic_info', 'has_pdf_capture', 'has_image', ]:
            value = getattr(news, field)
            self.assertFalse(value)

    def test_set_web_title(self):
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")
        self.assertEqual(news.title, '')
        news.set_web_title()
        self.assertNotEqual(news.title, '')

    def test_fetch_archived_url(self):
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")
        self.assertIsNone(news.archived_news_url)
        news.fetch_archived_url()
        self.assertIsNotNone(news.archived_news_url)

    def test_set_basic_info(self):
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")

        expected_response_keys = ['title', 'authors', 'body', 'teaser',
                                  'published_date', 'language', 'image', 'keywords', ]
        # Atributos que não podem estar em branco ('')
        not_blank_attrs = expected_response_keys[:2]
        # Atributos que não podem estar nulos (None)
        not_null_attrs = expected_response_keys[2:-2]
        # Atributos especiais, que começam com '_' e que não podem estar nulos (None)
        under_attrs = ['_{}'.format(key)
                       for key in expected_response_keys[-2:]]

        result = news.set_basic_info()

        for expected_key in expected_response_keys:
            self.assertIn(expected_key, result.keys())

        for not_blank_attr in not_blank_attrs:
            value = getattr(news, not_blank_attr)
            self.assertNotEqual(value, '')

        for not_null_attr in not_null_attrs:
            value = getattr(news, not_null_attr)
            self.assertIsNotNone(value)
            if not_null_attr == 'published_date':
                # 'published_date' deve ser do tipo data/tempo...
                self.assertIsInstance(value, datetime.datetime)
                # ...e deve conter informações do fuso-horário (não pode ser uma data ingênua)
                self.assertIsNotNone(news.published_date.tzinfo)

        for under_attr in under_attrs:
            value = getattr(news, under_attr)
            self.assertIsNotNone(value)
            if under_attr == '_keywords':
                # '_keywords' deve ser do tipo lista
                self.assertIsInstance(value, list)
