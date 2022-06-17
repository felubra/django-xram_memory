import os

from django.utils.six import BytesIO
from tempfile import gettempdir
from pdf2image import convert_from_path

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

    # Converta a primeira página do arquivo pdf e salve-a como arquivo temporário
    images = convert_from_path(
        source.path, first_page=0, last_page=1, output_folder=gettempdir()
    )

    # Não estou certo se images vai ter sempre apenas um arquivo gerado, então vamos verificar todos
    for index, image in enumerate(images):
        # só nos interessa usar a primeira página
        if index == 0:
            with open(image.filename, mode="rb") as f:
                source = BytesIO(f.read())
        # feche o arquivo temporário
        image.fp.close()
        # apague o arquivo temporário
        os.remove(image.filename)

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
