from django.urls import path


from assets.views import (
    AssetCategoryCreateView,
    AssetCategoryDeleteView,
    AssetCategoryDetailView,
    AssetCategoryListView,
    AssetCategoryUpdateView,
    BrandCreateView,
    BrandDeleteView,
    BrandDetailView,
    BrandListView,
    BrandUpdateView,

    AssetModelCreateView,
    AssetModelDeleteView,
    AssetModelDetailView,
    AssetModelListView,
    AssetModelUpdateView,
)
from assets.views import (
    AssetListView,
    AssetCreateView,
    AssetDetailView,
    AssetUpdateView,
    AssetDeleteView,
)

from assets.views import (
    AssetAssignmentListView,
    AssetAssignmentCreateView,
    AssetAssignmentDetailView,
    AssetAssignmentUpdateView,
    AssetReturnView,
)
from assets.views.asset_transfer import (
    AssetTransferListView,
    AssetTransferCreateView,
    AssetTransferDetailView,
    AssetTransferUpdateView,
)
from assets.views.asset_history import AssetHistoryListView
app_name = "assets"
urlpatterns = [
    path(
        "categories/",
        AssetCategoryListView.as_view(),
        name="asset-category-list",
    ),
    path(
        "categories/create/",
        AssetCategoryCreateView.as_view(),
        name="asset-category-create",
    ),
    path(
        "categories/<uuid:pk>/",
        AssetCategoryDetailView.as_view(),
        name="asset-category-detail",
    ),
    path(
        "categories/<uuid:pk>/edit/",
        AssetCategoryUpdateView.as_view(),
        name="asset-category-update",
    ),
    path(
        "categories/<uuid:pk>/delete/",
        AssetCategoryDeleteView.as_view(),
        name="asset-category-delete",
    ),

    # ============================================================
    # Brands
    # ============================================================

    path(
        "brands/",
        BrandListView.as_view(),
        name="brand-list",
    ),

    path(
        "brands/create/",
        BrandCreateView.as_view(),
        name="brand-create",
    ),

    path(
        "brands/<uuid:pk>/",
        BrandDetailView.as_view(),
        name="brand-detail",
    ),

    path(
        "brands/<uuid:pk>/edit/",
        BrandUpdateView.as_view(),
        name="brand-update",
    ),

    path(
        "brands/<uuid:pk>/delete/",
        BrandDeleteView.as_view(),
        name="brand-delete",
    ),

    # ==========================================================
    # Asset Models
    # ==========================================================

    path(
        "models/",
        AssetModelListView.as_view(),
        name="asset-model-list",
    ),

    path(
        "models/create/",
        AssetModelCreateView.as_view(),
        name="asset-model-create",
    ),

    path(
        "models/<uuid:pk>/",
        AssetModelDetailView.as_view(),
        name="asset-model-detail",
    ),

    path(
        "models/<uuid:pk>/edit/",
        AssetModelUpdateView.as_view(),
        name="asset-model-update",
    ),

    path(
        "models/<uuid:pk>/delete/",
        AssetModelDeleteView.as_view(),
        name="asset-model-delete",
    ),

# =====================================================
# Asset
# =====================================================

    path(
        "assets/",
        AssetListView.as_view(),
        name="asset-list",
    ),

    path(
        "assets/create/",
        AssetCreateView.as_view(),
        name="asset-create",
    ),

    path(
        "assets/<uuid:pk>/",
        AssetDetailView.as_view(),
        name="asset-detail",
    ),

    path(
        "assets/<uuid:pk>/update/",
        AssetUpdateView.as_view(),
        name="asset-update",
    ),

    path(
        "assets/<uuid:pk>/delete/",
        AssetDeleteView.as_view(),
        name="asset-delete",
    ),


    # =====================================================
# Asset Assignment
# =====================================================

path(
    "assignments/",
    AssetAssignmentListView.as_view(),
    name="asset-assignment-list",
),

path(
    "assignments/create/",
    AssetAssignmentCreateView.as_view(),
    name="asset-assignment-create",
),

path(
    "assignments/<uuid:pk>/",
    AssetAssignmentDetailView.as_view(),
    name="asset-assignment-detail",
),

path(
    "assignments/<uuid:pk>/update/",
    AssetAssignmentUpdateView.as_view(),
    name="asset-assignment-update",
),

path(
    "assignments/<uuid:pk>/return/",
    AssetReturnView.as_view(),
    name="asset-return",
),


# =====================================================
# Asset Transfer
# =====================================================

path(
    "transfers/",
    AssetTransferListView.as_view(),
    name="asset-transfer-list",
),

path(
    "transfers/create/",
    AssetTransferCreateView.as_view(),
    name="asset-transfer-create",
),

path(
    "transfers/<uuid:pk>/",
    AssetTransferDetailView.as_view(),
    name="asset-transfer-detail",
),

path(
    "transfers/<uuid:pk>/update/",
    AssetTransferUpdateView.as_view(),
    name="asset-transfer-update",
),
path(
    "assets/<uuid:pk>/history/",
    AssetHistoryListView.as_view(),
    name="asset-history",
),

]

# Create your models here.
