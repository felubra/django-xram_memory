from tempfile import gettempdir
from pdf2image import convert_from_path, convert_from_bytes
try:
    from PIL import Image
except ImportError:
    import Image


def pdf_preview(source, exif_orientation=True, **options):
    if not source:
        return
    images = convert_from_path(
        source.path, first_page=0, last_page=1)
    return images[0]
