from django.test import TestCase, TransactionTestCase
from xram_memory.artifact.models import Document
from django.core.files import File as DjangoFile
from django.db.models.signals import post_save
from filer import settings as filer_settings
from contextlib import contextmanager
from unittest.mock import patch
from loguru import logger
from pathlib import Path
import factory
import os
import magic


logger.remove()
# Create your tests here.


class DocumentTestCase(TransactionTestCase):
    serialized_rollback = True
    @contextmanager
    def open_as_django_file(self, filename):
        with open(filename, 'rb') as fd:
            django_file = DjangoFile(fd, name=filename)
            yield django_file

    def test_matches_all_filetypes(self):
        self.assertTrue(Document.matches_file_type(None, None, None))

    def test_initial_flags_state(self):
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
        document = Document()
        self.assertFalse(document.set_document_id())
        self.assertIsNone(document.document_id)

    @factory.django.mute_signals(post_save)
    def test_set_document_id_without_signals(self):
        image_file_path = Path(os.path.dirname(__file__), './files/image.jpg')
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
        image_file_path = Path(os.path.dirname(__file__), './files/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertIsNotNone(document.document_id)
            self.assertEqual(str(document), document.document_id.hashid)

    @factory.django.mute_signals(post_save)
    def test_determine_mime_type_without_signals(self):
        image_file_path = Path(os.path.dirname(__file__), './files/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.mime_type, '')
            self.assertTrue(document.determine_mime_type())
            self.assertEqual(document.mime_type, 'image/jpeg')
            # Se o mesmo mimetype que o anterior for constatado, a função deverá retornar False
            self.assertFalse(document.determine_mime_type())

    def test_determine_mime_type_after_normal_save(self):
        image_file_path = Path(os.path.dirname(__file__), './files/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            self.assertEqual(document.mime_type, 'image/jpeg')

    def test_determine_mime_type_with_failure(self):
        with patch.object(magic, 'from_buffer') as mocked_function:
            mocked_function.side_effect = os.error
            image_file_path = Path(os.path.dirname(
                __file__), './files/image.jpg')
            with self.open_as_django_file(image_file_path) as django_file:
                document = Document(file=django_file)
                self.assertFalse(document.determine_mime_type())
                self.assertEqual(document.mime_type, '')

    def test_thumbnails_presence_for_image_document(self):
        image_file_path = Path(os.path.dirname(__file__), './files/image.jpg')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            for size in Document.IMAGE_DOCUMENT_THUMBNAILS_ALIASES:
                self.assertIn(size, document.thumbnails.keys())

    def test_image_thumbnails_absence_for_pdf_document(self):
        image_file_path = Path(os.path.dirname(__file__), './files/pdf.pdf')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            for size in Document.IMAGE_DOCUMENT_THUMBNAILS_ALIASES:
                self.assertNotIn(size, document.thumbnails.keys())

    def test_for_filer_icon_thumbnails_presence(self):
        document = Document()
        self.assertEqual(document.icons, 'file')
        image_file_path = Path(os.path.dirname(__file__), './files/pdf.pdf')
        with self.open_as_django_file(image_file_path) as django_file:
            document = Document(file=django_file)
            document.save()
            for size in filer_settings.FILER_ADMIN_ICON_SIZES:
                self.assertIn(size, document.icons.keys())
            for generated_icon_url in document.icons.values():
                self.assertIsNotNone(generated_icon_url)
