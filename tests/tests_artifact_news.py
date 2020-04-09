from django.db.models.signals import post_save, m2m_changed, pre_delete, post_delete
from xram_memory.artifact.models import News, NewsImageCapture, NewsPDFCapture
from xram_memory.taxonomy.models import Keyword, Subject
from django.test import TestCase, TransactionTestCase
from filer.models.foldermodels import Folder
from xram_memory.lib import NewsFetcher
from contextlib import contextmanager
from django.conf import settings
from unittest.mock import patch
from loguru import logger
from . import fixtures
import datetime
import hashlib
import factory
import pytest

logger.remove()

# Create your tests here.

# TODO: Quando for buscar uma notícia na web, usar uma fixture, já que essa notícia pode ser retirada do ar
# TODO: converter para o estilo pytest quando https://github.com/pytest-dev/pytest-django/pull/721 for aceita


@factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
@pytest.mark.django_db(transaction=True)
class NewsTestCase(TransactionTestCase):
    serialized_rollback = True

    @contextmanager
    def basic_news(self):
        newspaper = fixtures.NewspaperFactory()
        newspaper.save()
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html", newspaper=newspaper)
        with patch.object(NewsFetcher, 'fetch_basic_info', return_value=fixtures.NEWS_INFO_MOCK):
            raw_news_data = news.set_basic_info()
        news.save()
        yield news, raw_news_data

    def test_require_url_on_save(self):
        """ Não deve ser possível salvar uma Notícia sem uma URL"""
        news = News(title="Abacate")
        self.assertRaises(ValueError, news.save)

    def test_save_without_title(self):
        """ Tentativa de salvar notícia sem título deve tentar buscar o título na web """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")

        with patch.object(NewsFetcher, 'fetch_web_title') as mocked:
            mocked.return_value = 'Dilma paga pedaladas até de 2015  para enfraquecer argumento do impeachment'
            news.save()
            self.assertTrue(mocked.called)
            self.assertEqual(news.title, mocked.return_value)

    def test_string_value(self):
        """ Testa a representação do objeto da notícia """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        self.assertEqual(str(news), '(sem título)')
        news.title = "Um teste"
        self.assertEqual(str(news), news.title)

    def test_initial_flags_state(self):
        """ Testa o estado inicial das propriedades do objeto Notícia """
        news = News(
            url="https://internacional.estadao.com.br/noticias/geral,venezuela-anuncia-reabertura-da-fronteira-com-brasil-e-aruba,70002823580")
        for field in ['thumbnail', 'published_year', 'image_capture_indexing', 'body', 'teaser', 'published_date', 'newspaper']:
            value = getattr(news, field)
            self.assertIsNone(value)

        for field in ['title', 'authors', ]:
            value = getattr(news, field)
            self.assertEqual(value, '')

        for field in ['has_basic_info', 'has_pdf_capture', 'has_image', ]:
            value = getattr(news, field)
            self.assertFalse(value)

    def test_fetch_archived_url(self):
        """ news.fetch_archived_url deve chamar NewsFetcher.fetch_archived_url e setar a propriedade News.archived_news_url """
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")
        self.assertIsNone(news.archived_news_url)
        with patch.object(NewsFetcher, 'fetch_archived_url') as mocked:
            mocked.return_value = fixtures.mocked_news_fetch_archived_url(
                news.url)
            news.fetch_archived_url()
            self.assertTrue(mocked.called)
            self.assertEqual(news.archived_news_url, mocked.return_value)

    def test_set_basic_info(self):
        """ News.set_basic_info deve chamar NewsFetcher.fetch_basic_info e setar as propriedades relacionadas """
        news = News(
            url="https://brasil.elpais.com/brasil/2015/12/29/economia/1451418696_403408.html")

        # Atributos que não podem estar em branco ('')
        not_blank_attrs = ['title', 'authors']
        # Atributos que não podem estar nulos (None)
        not_null_attrs = ['body', 'teaser', 'published_date', 'language']

        expected_response_keys = [
            *not_blank_attrs, *not_null_attrs]

        with patch.object(NewsFetcher, 'fetch_basic_info', return_value=fixtures.NEWS_INFO_MOCK):
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

    def test_add_fetched_keywords(self):
        """ News.add_fetched_keywords deve criar as palavras-chave e associá-las à notícia """
        with self.basic_news() as (news, raw_news_data,):
            news.add_fetched_keywords(raw_news_data['keywords'])
            self.assertIsNotNone(news.keywords.all())
            self.assertEqual(len(news.keywords.all()), len(raw_news_data['keywords']))

            for fetched_keyword in raw_news_data['keywords']:
                self.assertIsNotNone(Keyword.objects.get(name=fetched_keyword))

    def test_add_fetched_subjects(self):
        """ News.add_fetched_subject deve criar os assuntos e associá-los à notícia """
        with self.basic_news() as (news, raw_news_data,):
            news.add_fetched_subjects(raw_news_data['subjects'])
            self.assertIsNotNone(news.subjects.all())
            self.assertEqual(len(news.subjects.all()), len(raw_news_data['subjects']))

            for fetched_subject in raw_news_data['subjects']:
                self.assertIsNotNone(Subject.objects.get(name=fetched_subject))

    def test_keywords_indexing(self):
        """ News.keywords_indexing deve ser uma lista com as palavras-chave associadas """
        with self.basic_news() as (news, raw_news_data,):
            self.assertIsNotNone(news.keywords_indexing)
            self.assertIsInstance(news.keywords_indexing, list)
            self.assertEqual(len(news.keywords_indexing), 0)

            news.add_fetched_keywords(raw_news_data['keywords'])
            self.assertEqual(len(news.keywords_indexing), len(raw_news_data['keywords']))

            for fetched_keyword in raw_news_data['keywords']:
                self.assertIn(fetched_keyword, news.keywords_indexing)

    def test_subjects_indexing(self):
        """ News.subjects_indexing deve ser uma lista com os assuntos associados """
        with self.basic_news() as (news, raw_news_data,):
            self.assertIsNotNone(news.subjects_indexing)
            self.assertIsInstance(news.subjects_indexing, list)
            self.assertEqual(len(news.subjects_indexing), 0)

            news.add_fetched_subjects(raw_news_data['subjects'])
            self.assertEqual(len(news.subjects_indexing), len(raw_news_data['subjects']))

            for fetched_subject in raw_news_data['subjects']:
                self.assertIn(fetched_subject, news.subjects_indexing)

    def test_null_field_indexing(self):
        """ News.null_field_indexing deve retornar None """
        news = News()
        self.assertIsNone(news.null_field_indexing)

    @pytest.mark.django_db(transaction=True)
    def test_has_image_and_test_add_fetched_image(self):
        """ Testa News.has_image depois de adicionar uma imagem """
        with self.basic_news() as (news, raw_news_data,):
            news.add_fetched_image(raw_news_data['image'])
            self.assertTrue(news.has_image)

    @pytest.mark.django_db(transaction=True)
    def test_add_fetched_image(self):
        """ News.add_fetched_image deve gerar `NewsImageCapture` e associá-la a notícia """
        with self.basic_news() as (news, raw_news_data,):
            with patch.object(NewsFetcher, 'fetch_image') as mocked:
                with fixtures.mocked_news_add_fetched_image(raw_news_data['image']) as f:
                    mocked.return_value.__enter__.return_value = f
                    news.add_fetched_image(raw_news_data['image'])
                    self.assertIsNotNone(news.image_capture)
                    self.assertIsInstance(news.image_capture, NewsImageCapture)
                    self.assertIsNotNone(news.thumbnail)
                    self.assertIsNotNone(news.image_capture_indexing)

    @pytest.mark.django_db(transaction=True)
    def test_add_another_fetched_image(self):
        """ Uma notícia deve ter apenas uma captura de imagem """
        with self.basic_news() as (news, raw_news_data,):
            with patch.object(NewsFetcher, 'fetch_image') as mocked:
                with fixtures.mocked_news_add_fetched_image(raw_news_data['image']) as f:
                    mocked.return_value.__enter__.return_value = f
                    news.add_fetched_image(raw_news_data['image'])
                    first_image_capture_pk = news.image_capture.pk
                    news.add_fetched_image(raw_news_data['image'])
                    self.assertNotEqual(first_image_capture_pk,
                                        news.image_capture.pk)
                    with self.assertRaises(NewsImageCapture.DoesNotExist):
                        self.assertIsNone(
                            NewsImageCapture.objects.get(pk=first_image_capture_pk))

    @pytest.mark.django_db(transaction=True)
    def test_add_fetched_image_filename_generated_with_salt(self):
        """
        Um Documento de captura de imagem não pode ter o nome de seu arquivo original deduzível a
        partir de um hash simples sem sal. Em outras palavras, a função `add_fetched_image` deve
        sempre usar um sal na geração do nome do arquivo.
        TODO: revisar
        """
        with self.basic_news() as (news, raw_news_data,):
            with patch.object(NewsFetcher, 'fetch_image') as mocked:
                with fixtures.mocked_news_add_fetched_image(raw_news_data['image']) as f:
                    mocked.return_value.__enter__.return_value = f
                    hashed_image_filename = hashlib.md5(
                        raw_news_data['image'].encode('utf-8')).hexdigest()
                    news.add_fetched_image(raw_news_data['image'])
                    self.assertNotIn(hashed_image_filename, news.image_capture.image_document.name)

    @pytest.mark.django_db(transaction=True)
    def test_add_pdf_capture(self):
        """ Testa News.add_pdf_capture, inclusive com a adição de mais de uma captura """
        with self.basic_news() as (news, raw_news_data,):
            with patch.object(NewsFetcher, 'get_pdf_capture') as mocked:
                with fixtures.mocked_news_get_pdf_capture(raw_news_data['image']) as f:
                    mocked.return_value.__enter__.return_value = f
                    news.add_pdf_capture()
                    self.assertEqual(len(news.pdf_captures.all()), 1)
                    self.assertIsInstance(
                        news.pdf_captures.all()[0], NewsPDFCapture)
                    self.assertTrue(news.has_pdf_capture)
                    news.add_pdf_capture()
                    self.assertEqual(len(news.pdf_captures.all()), 2)
                    self.assertTrue(news.has_pdf_capture)
