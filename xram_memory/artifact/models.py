from polymorphic.models import PolymorphicModel
from ..base_models import TraceableModel


# Create your models here.
class Artifact(TraceableModel, PolymorphicModel):
    pass
