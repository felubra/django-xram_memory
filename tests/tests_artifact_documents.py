from django.db.models.signals import post_save, m2m_changed, pre_delete, post_delete
from django_elasticsearch_dsl.signals import RealTimeSignalProcessor
from django.test import TestCase, TransactionTestCase
from xram_memory.artifact.models import Document
from django.core.files import File as DjangoFile
from filer import settings as filer_settings
from contextlib import contextmanager
from unittest.mock import patch
from loguru import logger
from pathlib import Path
import factory
import magic
import os
import pytest


logger.remove()
# Create your tests here.


@pytest.mark.django_db(transaction=True)
class DocumentTestCase(TransactionTestCase):
    serialized_rollback = True

    @contextmanager
    def open_as_django_file(self, filename):
        """
        Lê um arquivo em `pathname` e retorna um gerenciador de contexto com este arquivo
        encapsulado em uma classe `File` do Django
        """
        with open(filename, 'rb') as fd:
            django_file = DjangoFile(fd, name=filename)
            yield django_file

    def test_matches_all_filetypes(self):
        """
        Um Documento deve sempre retornar essa função como True, pois irá lidar com qualquer tipo de
        arquivo.
        """
        self.assertTrue(Document.matches_file_type(None, None, None))

    def test_initial_flags_state(self):
        """
        Testa o estado inicial das propriedades de um documento vazio.
        """
        document = Document()
        for field in ['search_thumbnail', 'thumbnail', 'file_indexing', 'mime_type', 'document_id_indexing', 'icon']:
            value = getattr(document, field)
            self.assertEqual(value, '')

        for field in ['published_year', 'published_date']:
            value = getattr(document, field)
            self.assertIsNone(value)

        self.assertEqual(document.thumbnails, {})
        self.assertEqual(document.icons, 'file')
        self.assertEqual(str(document), 'None')

    def test_document_id_initial_state(self):
        """
        Testa o estado inicial de `document_id` e `set_document_id`
        """
        document = Document()
        self.assertFalse(document.set_document_id())
        self.assertIsNone(document.document_id)

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_set_document_id_without_signals(self):
        """
        Testa o funcionamento de `set_document_id` e o estado de `document_id` após a invocação
        dessa função. Desativa os sinais do django para poder controlar quando `set_document_id` é 
        invocada.
        """
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNone(document.document_id)
            self.assertTrue(document.set_document_id())
            self.assertIsNotNone(document.document_id)
            # Uma definido, um document_id não pode ser alterado e a função deve retornar False
            self.assertFalse(document.set_document_id())
            self.assertEqual(str(document), document.document_id.hashid)

    def test_set_document_id_after_normal_save(self):
        """
        Testa se `set_document_id` é invocada por um sinal depois de `Document.save()`.
        """
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNotNone(document.document_id)
            self.assertEqual(str(document), document.document_id.hashid)

    @factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
    def test_determine_mime_type_without_signals(self):
        """
        Testa o funcionamento de `determine_mime_type` e o estado de `mime_type` após a invocação
        dessa função. Desativa os sinais do django para poder controlar o momento em que
        `determine_mime_type` é invocada.
        """
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.mime_type, '')
            self.assertTrue(document.determine_mime_type())
            self.assertEqual(document.mime_type, 'image/jpeg')
            # Se o mesmo mimetype que o anterior for constatado, a função deverá retornar False
            self.assertFalse(document.determine_mime_type())

    def test_determine_mime_type_after_normal_save(self):
        """
        Testa se `determine_mime_type` é invocada por um sinal depois de `Document.save()`.
        """
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            with patch.object(Document, 'determine_mime_type') as mocked:
                mocked.return_value = 'image/jpeg'
                self.assertEqual(document.mime_type, 'image/jpeg')

    def test_determine_mime_type_with_failure(self):
        """
        Testa se uma possível falha em `determine_mime_type` será lidada corretamente.
        """
        with patch.object(magic, 'from_buffer') as mocked_function:
            mocked_function.side_effect = os.error
            image_file_path = Path(os.path.dirname(
                __file__), './fixtures/image.jpg')
            with self.open_as_django_file(image_file_path) as django_file:
                document = Document(file=django_file)
                self.assertFalse(document.determine_mime_type())
                self.assertEqual(document.mime_type, '')

    def test_for_filer_icon_thumbnails_presence(self):
        """
        Verifica se os tamanhos dos ícones usados pelo app Filer são gerados corretamente.
        """
        document = Document()
        self.assertEqual(document.icons, 'file')
        image_file_path = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            for size in filer_settings.FILER_ADMIN_ICON_SIZES:
                self.assertIn(size, document.icons.keys())
            for generated_icon_url in document.icons.values():
                self.assertIsNotNone(generated_icon_url)

    def test_if_document_saves_clear_thumbnails_caches(self):
        document = Document()
        self.assertEqual(document.thumbnail, '')
        self.assertEqual(document.search_thumbnail, '')
        self.assertEqual(document.icon, '')
        self.assertEqual(document.thumbnails, {})
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document.file = django_file
            document.save()
            thumbnail = document.thumbnail
            self.assertNotEqual(thumbnail, '')
            search_thumbnail = document.search_thumbnail
            self.assertNotEqual(search_thumbnail, '')
            icon = document.icon
            self.assertNotEqual(icon, '')
            thumbnails = document.thumbnails
            self.assertNotEqual(thumbnails, {})

            pdf_file_path = Path(os.path.dirname(
                __file__), './fixtures/pdf.pdf')
            with self.open_as_django_file(pdf_file_path) as django_file2:
                document.file = django_file2
                document.save()
                self.assertNotEqual(document.thumbnail, thumbnail)
                self.assertNotEqual(
                    document.search_thumbnail, search_thumbnail)
                self.assertNotEqual(document.icon, icon)
                self.assertNotEqual(document.thumbnails, thumbnails)

    def test_pdf_document_num_pages(self):
        """
        Testa a quantidade páginas informada para um documento em pdf
        """
        document = Document()
        self.assertIsNone(document.num_pages)
        three_page_pdf = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        five_page_pdf = Path(os.path.dirname(__file__),
                             './fixtures/five_page.pdf')
        with self.open_as_django_file(three_page_pdf) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.num_pages, 3)

        with self.open_as_django_file(five_page_pdf) as django_file:
            document.file = django_file
            self.assertEqual(document.num_pages, 3)
            document.save()
            self.assertEqual(document.num_pages, 5)

    def test_image_document_num_pages(self):
        """
        Testa a quantidade páginas informada para um documento de imagem
        """
        document = Document()
        self.assertIsNone(document.num_pages)
        image_file = Path(os.path.dirname(__file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.num_pages, 1)

    def test_unknown_document_num_pages(self):
        """
        Testa a quantidade páginas informada para um documento de imagem
        """
        document = Document()
        self.assertIsNone(document.num_pages)
        text_file = Path(os.path.dirname(__file__), './fixtures/text.txt')
        with self.open_as_django_file(text_file) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.num_pages, 1)

    def test_pdf_file_page_previews(self):
        """
        Testa a geração de imagens para cada página num arquivo pdf.
        """
        document = Document()
        self.assertIsNone(document.pages)
        five_page_pdf = Path(os.path.dirname(__file__),
                             './fixtures/five_page.pdf')
        three_page_pdf = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        with self.open_as_django_file(five_page_pdf) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNotNone(document.pages)
            self.assertEqual(len(document.pages), document.num_pages)

        with self.open_as_django_file(three_page_pdf) as django_file:
            document.file = django_file
            document.save()
            self.assertIsNotNone(document.pages)
            self.assertEqual(len(document.pages), document.num_pages)

    def test_unknown_file_pages(self):
        """
        Um documento do tipo que não seja pdf deve retornar None
        """
        document = Document()
        self.assertIsNone(document.pages)
        text_file = Path(os.path.dirname(__file__), './fixtures/text.txt')
        three_page_pdf = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        with self.open_as_django_file(text_file) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNone(document.pages)

        with self.open_as_django_file(three_page_pdf) as django_file:
            document.file = django_file
            document.save()
            self.assertIsNotNone(document.pages)
            self.assertEqual(len(document.pages), document.num_pages)

    def test_pages_file_mime_type(self):
        """
        O mimetype do documento da página deve ser uma imagem jpeg.
        """
        three_page_pdf = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        with self.open_as_django_file(three_page_pdf) as django_file:
            document = Document(file=django_file)
            document.save()
            for page in document.pages:
                self.assertEqual(page.mime_type, 'image/jpeg')

    def test_document_delete_pages(self):
        """
        Os arquivos das imagens das páginas ser deletados quando um documento for salvo.
        """
        three_page_pdf = Path(os.path.dirname(__file__), './fixtures/pdf.pdf')
        generated_files = []
        with self.open_as_django_file(three_page_pdf) as django_file:
            document = Document(file=django_file)
            document.save()
            for page in document.pages:
                self.assertTrue(os.path.exists(page.file.path))
                generated_files.append(page.file.path)
            document.save()
            for generated_file in generated_files:
                self.assertFalse(os.path.exists(generated_file))
