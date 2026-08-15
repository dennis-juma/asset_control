from django.urls import path

from assets.views.asset_import import AssetImportView
from assets.views import (
    AssetCategoryCreateView,
    AssetCategoryDeleteView,
    AssetCategoryDetailView,
    AssetCategoryListView,
    AssetCategoryUpdateView,
    AssetCategoryBulkUpdateView,
    BrandCreateView,
    BrandDeleteView,
    BrandDetailView,
    BrandListView,
    BrandUpdateView,
    BrandBulkUpdateView,

    AssetModelCreateView,
    AssetModelDeleteView,
    AssetModelDetailView,
    AssetModelListView,
    AssetModelUpdateView,
    AssetModelBulkUpdateView,
)
from assets.views import (
    AssetListView,
    AssetCreateView,
    AssetDetailView,
    AssetUpdateView,
    AssetDeleteView,
    AssetBulkUpdateView,
    AssetExportView
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
from assets.views.asset_history import (
    AssetHistoryListView,
    AssetHistoryDetailView,
)

from assets.views.asset_attachment import (
    AssetAttachmentCreateView,
    AssetAttachmentDetailView,
    AssetAttachmentUpdateView,
    AssetAttachmentDeleteView,
)
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
        "categories/bulk-update/",
        AssetCategoryBulkUpdateView.as_view(),
        name="asset-category-bulk-update",
    ),
    path(
    "import/",
    AssetImportView.as_view(),
    name="asset-import",
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
        "brands/bulk-update/",
        BrandBulkUpdateView.as_view(),
        name="brand-bulk-update",
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
        "models/bulk-update/",
        AssetModelBulkUpdateView.as_view(),
        name="asset-model-bulk-update",
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
    "",
    AssetListView.as_view(),
    name="asset-list",
),
path(
    "export/",
    AssetExportView.as_view(),
    name="asset-export",
),

path(
    "create/",
    AssetCreateView.as_view(),
    name="asset-create",
),

path(
    "bulk-update/",
    AssetBulkUpdateView.as_view(),
    name="asset-bulk-update",
),

path(
    "<uuid:pk>/",
    AssetDetailView.as_view(),
    name="asset-detail",
),

path(
    "<uuid:pk>/update/",
    AssetUpdateView.as_view(),
    name="asset-update",
),

path(
    "<uuid:pk>/delete/",
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
path(
    "history/uuid:<uuid:pk>/",
    AssetHistoryDetailView.as_view(),
    name="asset-history-detail",
),
path(
    "attachments/create/",
    AssetAttachmentCreateView.as_view(),
    name="asset-attachment-create",
),

path(
    "attachments/<uuid:pk>/",
    AssetAttachmentDetailView.as_view(),
    name="asset-attachment-detail",
),

path(
    "attachments/<uuid:pk>/update/",
    AssetAttachmentUpdateView.as_view(),
    name="asset-attachment-update",
),

path(
    "attachments/<uuid:pk>/delete/",
    AssetAttachmentDeleteView.as_view(),
    name="asset-attachment-delete",
),

]

# Create your models here.
