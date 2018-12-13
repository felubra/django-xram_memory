from django.test import TestCase, Client
from .models import ArchivedNews, Keyword
from django.template.defaultfilters import slugify
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from .admin import ArchivedNewsAdmin
from ..users.models import User
from django.urls import reverse
from django.db import transaction


# Create your tests here.

class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


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


class KeywordTestCase(TestCase):
    def setUp(self):
        self.keyword = Keyword.objects.create(name="Abacate é uma fruta")

    def test_keyword_slug(self):
        '''Teste que a slug está sendo criada depois de o modelo ser salvo'''
        self.assertEqual(self.keyword.slug, slugify("Abacate é uma fruta"))


class ArchivedNewsAdminFormTestCase(TestCase):
    def setUp(self):
        self.automatic_archived_news = ArchivedNews(
            url="https://politica.estadao.com.br/noticias/geral,em-diplomacao-bolsonaro-diz-que-a-soberania-do-voto-popular-e-inquebrantavel,70002640605")
        self.site = AdminSite()
        self.user_info = {
            'username': 'admin',
            'email': 'test@test.com',
            'password': 'test@test.com'
        }
        self.user = User.objects.create_superuser(**self.user_info)
        self.client = Client()

    def test_fields_for_new_item(self):
        '''Testa a presença/ausência e os valores dos campos quando em modo de inserção'''
        archived_news_admin = ArchivedNewsAdmin(ArchivedNews, self.site)
        base_fields = archived_news_admin.get_form(request).base_fields

        # Verifica que o nosso campo 'virtual' 'insertion_mode' está presente no formulário
        self.assertIn('insertion_mode', base_fields)

    # @todo
    def test_fields_for_existing_item(self):
        '''Testa a presença/ausência e os valores dos campos quando em modo de edição'''
        with transaction.atomic():
            self.automatic_archived_news.save()
        #archived_news_admin = ArchivedNewsAdmin(ArchivedNews, self.site)
        # Crie um cliente para entrar na interface administrativa
        c = Client()
        # Faça login com o nosso usuário super administrador criado
        c.login(**self.user_info)
        archived_news_change_url = reverse(
            "admin:archived_news_archivednews_change", args=[self.automatic_archived_news.pk])
        response = c.get(archived_news_change_url)
        admin_form = response.context_data['adminform']
        pass
