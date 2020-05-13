from configurations.values import Value, ValidationMixin, SecretValue
from django.core.exceptions import ValidationError

class LunrBackendValue(ValidationMixin, Value):
    VALID_BACKENDS=['remote', 'local']

    @classmethod
    def validator(cls, value):
        if value not in cls.VALID_BACKENDS:
            raise ValidationError('Backend inválido')

    @property
    def message(self):
        return f'Backend inválido "{self.value}". Backends válidos: {", ".join(self.VALID_BACKENDS)}.'
