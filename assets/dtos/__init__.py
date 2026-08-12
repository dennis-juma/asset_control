from .asset_row import AssetRowDTO
from .asset_statistics import AssetStatisticsDTO
from .asset_list import AssetListDTO
from .asset_category import (
    AssetCategoryCreateDTO,
    AssetCategoryUpdateDTO,
)
from .brand import (
    BrandCreateDTO,
    BrandUpdateDTO,
)
from .asset_attachment import (
    AssetAttachmentCreateDTO,
    AssetAttachmentUpdateDTO,
)

from .asset_model import (
    AssetModelCreateDTO,
    AssetModelUpdateDTO,
)
from .asset import (
    AssetCreateDTO,
    AssetUpdateDTO,
)
from .asset_assignment import (
    AssetAssignmentCreateDTO,
    AssetAssignmentUpdateDTO,
    AssetReturnDTO,
)


__all__ = [
    "AssetRowDTO",
    "AssetStatisticsDTO",
    "AssetListDTO",
    "AssetCategoryCreateDTO",
    "AssetCategoryUpdateDTO",
    "BrandCreateDTO",
    "BrandUpdateDTO",
    "AssetModelCreateDTO",
    "AssetModelUpdateDTO",

    "AssetCreateDTO",
    "AssetUpdateDTO"

    "AssetAssignmentCreateDTO",
    "AssetAssignmentUpdateDTO",
    "AssetReturnDTO",

    "AssetAttachmentCreateDTO",
   "AssetAttachmentUpdateDTO",

   "AssetDetailContentDTO"
    

    

]