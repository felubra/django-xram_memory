from configurations.values import Value, ValidationMixin
from django.core.exceptions import ValidationError

class LunrBackendValue(ValidationMixin, Value):
    BACKEND_LOCAL = 'local'
    BACKEND_REMOTE = 'remote'
    VALID_BACKENDS=[BACKEND_REMOTE, BACKEND_LOCAL]

    @classmethod
    def validator(cls, value):
        if value not in cls.VALID_BACKENDS:
            raise ValidationError('Backend inválido')

    @property
    def message(self):
        return f'Backend inválido "{self.value}". Backends válidos: {", ".join(self.VALID_BACKENDS)}.'
