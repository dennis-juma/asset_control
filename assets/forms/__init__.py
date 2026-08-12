from .asset_category import (
    AssetCategoryCreateForm,
    AssetCategoryUpdateForm,
)
from .brand import (
    BrandCreateForm,
    BrandUpdateForm,
)
from .asset_model import (
    AssetModelCreateForm,
    AssetModelUpdateForm,
)

from .asset import (
    AssetCreateForm,
    AssetUpdateForm,
)
from .asset_assignment import (
    AssetAssignmentCreateForm,
    AssetAssignmentUpdateForm,
    AssetReturnForm,
)
from .transfer import (
    AssetTransferCreateForm,
)
from .asset_attachment import (
    AssetAttachmentCreateForm,
    AssetAttachmentUpdateForm,
)
from .asset_history import AssetHistoryDetailForm

__all__ = [
    "AssetCategoryCreateForm",
    "AssetCategoryUpdateForm",
    "BrandCreateForm",
    "BrandUpdateForm",
    "AssetModelCreateForm",
    "AssetModelUpdateForm",
    "AssetCreateForm",
    "AssetUpdateForm",
    "AssetAssignmentCreateForm",
    "AssetAssignmentUpdateForm",
    "AssetReturnForm",
    "AssetTransferCreateForm"

    "AssetAttachmentCreateForm",
   " AssetAttachmentUpdateForm",

   "AssetHistoryDetailForm"
]