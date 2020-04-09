from xram_memory.search_indexes.documents.document import DocumentDocument
from xram_memory.artifact.models import Document
from django.core.files import File as DjangoFile
from contextlib import contextmanager
from pathlib import Path
import pytest
import os


@contextmanager
def open_as_django_file(filename):
    """
    Lê um arquivo em `pathname` e retorna um gerenciador de contexto com este arquivo
    encapsulado em uma classe `File` do Django
    """
    with open(filename, 'rb') as fd:
        django_file = DjangoFile(fd, name=filename)
        yield django_file


@pytest.mark.last
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_non_user_document_indexed():
    """
    Testa se um documento marcado como não sendo do usuário não está sendo indexado pelo Elastic Search.
    NOTA: Este teste requer que o serviço do Elastic Search esteja rodando conforme definido na configuração.
    """
    pdf_file_path = Path(os.path.dirname(
        __file__), './fixtures/pdf.pdf')
    with open_as_django_file(pdf_file_path) as django_file:
        document = Document(is_user_object=False, file=django_file)

        # salve o documento para descobrirmos o seu hashid
        document.save()

        def fetch_es_document_by_id(doc_id):
            return DocumentDocument.search().query("match", document_id=doc_id)

        # apague qualquer documento com o mesmo hashid
        s = fetch_es_document_by_id(document.document_id_indexing)
        s.delete()
        assert s.count() == 0

        # salve o documento novamente, desta vez para fazer o teste de fato
        document.save()
        s = fetch_es_document_by_id(document.document_id_indexing)
        assert s.count() == 0
