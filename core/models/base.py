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
    Abstract base model for all business entities.

    Features:
    - UUID primary key
    - Created/Updated timestamps
    - Created by / Updated by tracking
    - Soft delete support
    - Active/Inactive status
    - Automatic slug generation
    """
    class Meta:
        abstract = True