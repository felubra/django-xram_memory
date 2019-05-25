from xram_memory.lib.file_previews import icon_preview, pdf_preview
from PIL.ImageFile import ImageFile
from dataclasses import dataclass
from django.test import TestCase
import pathlib
import os


@dataclass
class MockedSource:
    path: str


class FilePreviewsTests(TestCase):
    def test_icon_preview(self):
        result = icon_preview(MockedSource(
            path=os.path.join(os.path.dirname(__file__), "fixtures", "image.jpg")))
        self.assertIsInstance(result, ImageFile)

    def test_pdf_preview(self):
        result = pdf_preview(MockedSource(
            path=os.path.join(os.path.dirname(__file__), "fixtures", "pdf.pdf")))
        self.assertIsInstance(result, ImageFile)
