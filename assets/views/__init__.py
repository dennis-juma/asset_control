from .asset_list import AssetListView
from .asset import *
from .asset_category import (
    AssetCategoryCreateView,
    AssetCategoryDeleteView,
    AssetCategoryDetailView,
    AssetCategoryListView,
    AssetCategoryUpdateView,
)
from .brand import (
    BrandCreateView,
    BrandDeleteView,
    BrandDetailView,
    BrandListView,
    BrandUpdateView,
)
from .asset_model import (
    AssetModelCreateView,
    AssetModelDeleteView,
    AssetModelDetailView,
    AssetModelListView,
    AssetModelUpdateView,
)
from .asset_assignment import *
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
    "AssetHistoryListView"
    
    

]
