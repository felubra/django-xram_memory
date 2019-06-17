from django.core.exceptions import ValidationError
from xram_memory.quill_widget import no_empty_html
from pytest import raises

# Create your tests here.


def test_if_works():
    with raises(ValidationError):
        no_empty_html("<p></p>")


def test_if_works_with_spaces():
    with raises(ValidationError):
        no_empty_html("<p> </p>")


def test_if_works_with_spaces2():
    with raises(ValidationError):
        no_empty_html("<p>&nbsp;</p>")
