from xram_memory.lib.file_previews import icon_preview, pdf_preview
from PIL.ImageFile import ImageFile
from dataclasses import dataclass
import os


@dataclass
class MockedSource:
    path: str


def test_icon_preview():
    """
    Verifica se uma prévisualização de ícone de uma imagem jpeg é uma instância
    de ImageFile
    """
    result = icon_preview(MockedSource(
        path=os.path.join(os.path.dirname(__file__), "fixtures", "image.jpg")))
    assert isinstance(result, ImageFile)


def test_pdf_preview():
    """
    Verifica se uma prévisualização de ícone de um arquivo pdf é uma instância
    de ImageFile
    """
    result = pdf_preview(MockedSource(
        path=os.path.join(os.path.dirname(__file__), "fixtures", "pdf.pdf")))
    assert isinstance(result, ImageFile)
