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


def icon_preview(source, exif_orientation=True, **options):
    """
    Com base num arquivo de entrada, determina seu tipo e retorna um ícone.
    """
    if not source:
        return

    # retorne o caminho completo de um ícone do pacote file-icon-vectors
    def get_icon(icon_name):
        icon_file = finders.find(
            'file-icon-vectors/dist/icons/vivid/{icon}.svg'.format(icon=icon_name))
        return icon_file

    # aqui é suficiente pegar o mimetype do arquivo usando a biblioteca embutida do python, já que o arquivo já foi
    # enviado e, portanto, teve seu mimetype validado.
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
