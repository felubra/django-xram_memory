from xram_memory.artifact.models import News, NewsImageCapture, NewsPDFCapture
from xram_memory.taxonomy.models import Keyword, Subject
from django.test import TestCase, TransactionTestCase
from contextlib import contextmanager
from loguru import logger
import datetime
import hashlib

logger.remove()

# Create your tests here.

# TODO: Quando for buscar uma notícia na web, usar uma fixture, já que essa notícia pode ser retirada do ar


class NewsTestCase(TestCase):
    @contextmanager
    def basic_news(self):
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")
        news.set_basic_info()
        news.save()
        yield news

    def test_require_url_on_save(self):
        news = News(title="Abacate")
        self.assertRaises(ValueError, news.save)

    def test_save_without_title(self):
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        news.save()
        self.assertNotEqual(news.title, '')

    def test_string_value(self):
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        self.assertEqual(str(news), '(sem título)')
        news.title = "Um teste"
        self.assertEqual(str(news), news.title)

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

    def test_add_fetched_keywords(self):
        with self.basic_news() as news:
            self.assertIsNotNone(news._keywords)
            news.add_fetched_keywords()
            self.assertIsNotNone(news.keywords.all())
            self.assertEqual(len(news.keywords.all()), len(news._keywords))

            for fetched_keyword in news._keywords:
                self.assertIsNotNone(Keyword.objects.get(name=fetched_keyword))

    def test_add_fetched_keywords_with_preexisting_keyword(self):
        with self.basic_news() as news:
            self.assertIsNotNone(news._keywords)
            self.assertIn('2015', news._keywords)
            Keyword.objects.create(name='2015')
            news.add_fetched_keywords()
            self.assertIsNotNone(news.keywords.all())
            self.assertEqual(len(news.keywords.all()), len(news._keywords))

    def test_keywords_indexing(self):
        with self.basic_news() as news:
            self.assertIsNotNone(news.keywords_indexing)
            self.assertIsInstance(news.keywords_indexing, list)
            self.assertEqual(len(news.keywords_indexing), 0)

            news.add_fetched_keywords()
            self.assertEqual(len(news.keywords_indexing), len(news._keywords))

            for fetched_keyword in news._keywords:
                self.assertIn(fetched_keyword, news.keywords_indexing)

    def test_subjects_indexing(self):
        with self.basic_news() as news:
            self.assertIsNotNone(news.subjects_indexing)
            self.assertIsInstance(news.subjects_indexing, list)
            self.assertEqual(len(news.subjects_indexing), 0)

            politica_subject = Subject.objects.create(name="Política")
            news.subjects.add(politica_subject)
            self.assertEqual(len(news.subjects_indexing), 1)
            self.assertEqual(news.subjects_indexing, ['Política'])

    def test_null_field_indexing(self):
        news = News()
        self.assertIsNone(news.null_field_indexing)

    def test_has_image_and_test_add_fetched_image(self):
        with self.basic_news() as news:
            news.add_fetched_image()
            self.assertTrue(news.has_image)

    def test_add_fetched_image(self):
        with self.basic_news() as news:
            news.add_fetched_image()
            self.assertIsNotNone(news.image_capture)
            self.assertIsInstance(news.image_capture, NewsImageCapture)
            self.assertIsNotNone(news.thumbnail)
            self.assertIsNotNone(news.image_capture_indexing)

    def test_add_another_fetched_image(self):
        with self.basic_news() as news:
            news.add_fetched_image()
            first_image_capture_pk = news.image_capture.pk
            news.add_fetched_image()
            self.assertNotEqual(first_image_capture_pk, news.image_capture.pk)
            with self.assertRaises(NewsImageCapture.DoesNotExist):
                self.assertIsNone(
                    NewsImageCapture.objects.get(pk=first_image_capture_pk))

    def test_add_fetched_image_filename_generated_with_salt(self):
        """
        Um Documento de captura de imagem não pode ter o nome de seu arquivo original deduzível a
        partir de um hash simples sem sal. Em outras palavras, a função `add_fetched_image` deve
        sempre usar um sal na geração do nome do arquivo.
        """
        with self.basic_news() as news:
            hashed_image_filename = hashlib.md5(
                news._image.encode('utf-8')).hexdigest()
            news.add_fetched_image()
            self.assertNotIn(hashed_image_filename,
                             news.image_capture.image_document.name)

    def test_add_pdf_capture(self):
        with self.basic_news() as news:
            news.add_pdf_capture()
            self.assertEqual(len(news.pdf_captures.all()), 1)
            self.assertIsInstance(news.pdf_captures.all()[0], NewsPDFCapture)
            self.assertTrue(news.has_pdf_capture)
            news.add_pdf_capture()
            self.assertEqual(len(news.pdf_captures.all()), 2)
            self.assertTrue(news.has_pdf_capture)
