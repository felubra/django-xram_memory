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


@factory.django.mute_signals(post_save, m2m_changed, pre_delete, post_delete)
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

    def test_save_sets_mime_type_and_document_id(self):
        """
        Testa se, depois de salvo, um documento sempre terá um mime_type e document_id
        """
        image_file_path = Path(os.path.dirname(
            __file__), './fixtures/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNotNone(document.document_id)
            self.assertIsNotNone(document.mime_type)
            self.assertEqual(str(document), document.document_id.hashid)



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
