from django.test import TestCase
from .models import ArchivedNews

# Create your tests here.


class ArchivedNewsTestCase(TestCase):
    def setUp(self):
        self.archived_news = ArchivedNews(
            url="https://politica.estadao.com.br/noticias/geral,em-diplomacao-bolsonaro-diz-que-a-soberania-do-voto-popular-e-inquebrantavel,70002640605")

    def test_flags(self):
        '''Teste o estado inicial das flags'''
        self.assertEqual(self.archived_news.has_error, False)
        self.assertEqual(self.archived_news.needs_reprocessing, True)
        self.assertEqual(self.archived_news.has_basic_info, False)
        self.assertEqual(self.archived_news.has_pdf_capture, False)
        self.assertEqual(self.archived_news.has_web_archive, False)
        self.assertEqual(self.archived_news.is_published, False)
        self.assertEqual(self.archived_news.is_processed, False)
        self.assertEqual(self.archived_news.is_queued, False)
        self.assertEqual(self.archived_news.is_new, True)
