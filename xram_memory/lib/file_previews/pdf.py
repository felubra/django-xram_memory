import os
import mimetypes
from cairosvg import svg2png
from tempfile import mktemp
from contextlib import contextmanager

from django.utils.six import BytesIO
from tempfile import gettempdir
from pdf2image import convert_from_path, convert_from_bytes
from django.contrib.staticfiles import finders

try:
    from PIL import Image
except ImportError:
    import Image


def pdf_preview(source, exif_orientation=True, **options):
    """
    Com base num arquivo PDF de entrada, retorna uma imagem com a visualização da primeira página.
    """
    if not source:
        return

    # Pegue a imagem da primeira página do documento pdf
    with generate_pdf_page_thumbnails(source) as images:
        cover_image = images[0]
        with open(cover_image.filename, mode="rb") as f:
            source = BytesIO(f.read())

        # Código de https://github.com/SmileyChris/easy-thumbnails/blob/master/easy_thumbnails/source_generators.py
        image = Image.open(source)
        try:
            # An "Image file truncated" exception can occur for some images that
            # are still mostly valid -- we'll swallow the exception.
            image.load()
        except IOError:
            pass
        # Try a second time to catch any other potential exceptions.
        image.load()

        return image


@contextmanager
def generate_pdf_page_thumbnails(source, first_page=0, last_page=1, delete_after_exit=True):
    """
    Com base num arquivo PDF de entrada, retorna um gerenciador de contexto com os arquivos
    das visualizações de página gerados
    """
    if not source:
        return

    # Gere uma lista de imagens das páginas do PDF
    images = convert_from_path(
        source.path, first_page=first_page, last_page=last_page, output_folder=gettempdir())
    # Retorne a lista
    yield images

    if delete_after_exit:
        # Apague os arquivos das imagens geradas
        for index, image in enumerate(images):
            image.fp.close()
            os.remove(image.filename)
