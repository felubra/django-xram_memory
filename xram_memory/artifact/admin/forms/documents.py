import magic

from django import forms
from xram_memory.artifact.models import Document


class PDFDocumentAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(PDFDocumentAdminForm, self).clean()
        # Arquivos enviados devem ser PDFs de verdade
        file = cleaned_data.get('file', None)
        if file:
            file_mime = magic.from_buffer(file.read(1024), True)
            if 'application/pdf' != file_mime:
                self.add_error('file', 'Arquivo PDF inválido')


class ImageDocumentAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ImageDocumentAdminForm, self).clean()
        # Arquivos enviados devem ser imagens de verdade
        file = cleaned_data.get('file', None)
        if file:
            file_mime = magic.from_buffer(file.read(1024), True)
            if not 'image/' in file_mime:
                self.add_error('file', 'Imagem inválida')
