import os
import mimetypes
from cairosvg import svg2png
from tempfile import mktemp

from django.utils.six import BytesIO
from tempfile import gettempdir
from pdf2image import convert_from_path, convert_from_bytes
from django.contrib.staticfiles import finders

try:
    from PIL import Image
except ImportError:
    import Image


def pdf_preview(source, exif_orientation=True, **options):
    if not source:
        return

    # Converta a primeira página do arquivo pdf e salve-a como arquivo temporário
    images = convert_from_path(
        source.path, first_page=0, last_page=1, output_folder=gettempdir())

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


def icon_preview(source, exif_orientation=True, **options):
    if not source:
        return

    # retorne o caminho completo de um ícone do pacote file-icon-vectors
    def get_icon(icon_name):
        icon_file = finders.find(
            'file-icon-vectors/dist/icons/vivid/{icon}.svg'.format(icon=icon_name))
        return icon_file

    # aqui é suficiente pegar o mimetype do arquivo usando a biblioteca embutida do python, já que o arquivo já foi enviado.
    mimetype, _ = mimetypes.guess_type(source.path)
    extension = mimetypes.guess_extension(
        mimetype)[1:] if mimetypes.guess_extension(mimetype) is not None else 'blank'

    svg_icon = get_icon(extension)

    # crie um arquivo temporário para guardar o png convertido, leia ele e retorne o objeto PIL Image
    temp_file = mktemp()
    svg2png(url=svg_icon, write_to=temp_file)
    with open(temp_file, mode="rb") as f:
        source = BytesIO(f.read())
    os.remove(temp_file)

    image = Image.open(source)
    return image
