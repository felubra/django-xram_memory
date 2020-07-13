"""
Testa o validador no_empty_url.
Ele deve levantar ValidationError no caso de uma string com apenas tags
html, que convertida para texto, resultaria numa string vazia.
"""
from django.core.exceptions import ValidationError
from xram_memory.utils import no_empty_html
from pytest import raises



def test_with_only_tags():
    """
    Testa o caso do texto com apenas tags, sem conteúdo entre elas
    """
    with raises(ValidationError):
        no_empty_html("<p></p>")


def test_with_spaces_between_tags():
    """
    Testa o caso de um espaço em branco entre as tags
    """
    with raises(ValidationError):
        no_empty_html("<p> </p>")


def test_with_html_space_entity_between_tags():
    """
    Testa o caso de um símbolo de espaço em branco entre as tags
    """
    with raises(ValidationError):
        no_empty_html("<p>&nbsp;</p>")
