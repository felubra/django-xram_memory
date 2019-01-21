import magic

from django import forms
from xram_memory.artifact.models import Document

# TODO: refatorar classes abaixo para retirar código reptetido


class PDFDocumentAdminForm(forms.ModelForm):
    def clean(self):
        """
        Valide se o arquivo enviado é um PDF válido.
        """
        cleaned_data = super(PDFDocumentAdminForm, self).clean()
        # Arquivos enviados devem ser PDFs de verdade
        file = cleaned_data.get('file', None)
        if file:
            # leia 1024 bytes do arquivo para determinar seu tipo
            file_mime = magic.from_buffer(file.read(1024), True)
            if 'application/pdf' != file_mime:
                self.add_error('file', 'Arquivo PDF inválido')


class ImageDocumentAdminForm(forms.ModelForm):
    def clean(self):
        """
        Valide se o arquivo enviado é uma imagem válida.
        """
        cleaned_data = super(ImageDocumentAdminForm, self).clean()
        # Arquivos enviados devem ser imagens de verdade
        file = cleaned_data.get('file', None)
        if file:
            # leia 1024 bytes do arquivo para determinar seu tipo
            file_mime = magic.from_buffer(file.read(1024), True)
            if not 'image/' in file_mime:
                self.add_error('file', 'Imagem inválida')
