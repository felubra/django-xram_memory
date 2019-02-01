from django.test import TestCase
from django.core.exceptions import ValidationError
from . import no_empty_html

# Create your tests here.


class ValidatorTestCase(TestCase):
    def test_if_works(self):
        with self.assertRaises(ValidationError):
            no_empty_html("<p></p>")

    def test_if_works_with_spaces(self):
        with self.assertRaises(ValidationError):
            no_empty_html("<p> </p>")

    def test_if_works_with_spaces2(self):
        with self.assertRaises(ValidationError):
            no_empty_html("<p>&nbsp;</p>")
