from .asset_list import AssetListView
from .asset import *
from .asset_category import (
    AssetCategoryCreateView,
    AssetCategoryDeleteView,
    AssetCategoryDetailView,
    AssetCategoryListView,
    AssetCategoryUpdateView,
    AssetCategoryBulkUpdateView,
)
from .asset_import import AssetImportView
from .asset import AssetExportView
from .brand import (
    BrandCreateView,
    BrandDeleteView,
    BrandDetailView,
    BrandListView,
    BrandUpdateView,
    BrandBulkUpdateView,
)
from .asset_model import (
    AssetModelCreateView,
    AssetModelDeleteView,
    AssetModelDetailView,
    AssetModelListView,
    AssetModelUpdateView,
    AssetModelBulkUpdateView,
)
from .asset_attachment import (
    AssetAttachmentCreateView,
    AssetAttachmentDetailView,
    AssetAttachmentUpdateView,
    AssetAttachmentDeleteView,
)
from .asset_assignment import (
    AssetAssignmentListView,
    AssetAssignmentCreateView,
    AssetAssignmentDetailView,
    AssetAssignmentUpdateView,
    AssetAssignmentImportView,
    AssetAssignmentExportView,
    AssetReturnView,
)
from .asset_history import AssetHistoryListView


__all__ = [
    "AssetListView",
    "AssetCategoryListView",
    "AssetCategoryCreateView",
    "AssetCategoryDetailView",
    "AssetCategoryUpdateView",
    "AssetCategoryDeleteView",
    "BrandListView",
    "BrandCreateView",
    "BrandDetailView",
    "BrandUpdateView",
    "BrandDeleteView",
    "AssetModelCreateView",
    "AssetModelDeleteView"
    "AssetModelDetailView",
    "AssetModelListView",
    "AssetModelUpdateView",
    "AssetHistoryListView",

    "AssetAttachmentCreateView",
    "AssetAttachmentDetailView",
    "AssetAttachmentUpdateView",
    "AssetAttachmentDeleteView",
    "AssetExportView",

    "AssetImportView",
    
    

]
