from .active import IsActiveModel
from .audit import UserTrackingModel
from .soft_delete import SoftDeleteModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel
from .slug import SlugModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    UserTrackingModel,
    SoftDeleteModel,
    IsActiveModel,
    SlugModel,
    
):
    
    """
    Base model inherited by all business models.
    Provides:
    - UUID primary key
    - Audit fields
    - Soft delete
    - Active status
    - Slug generation
    """
    class Meta:
        abstract = True