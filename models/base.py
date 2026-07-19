from .audit import UserTrackingModel
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    UserTrackingModel,
    SoftDeleteModel,
):

    class Meta:
        abstract = True