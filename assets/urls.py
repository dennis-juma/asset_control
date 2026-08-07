from django.urls import path

from assets.views.asset_list import AssetListView
from assets.views.transfer import AssetTransferView
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

app_name = "assets"
urlpatterns = [
    path(
        "transfer/<int:pk>/",
        AssetTransferView.as_view(),
        name="asset-transfer",
    ),
    path("", AssetListView.as_view(), name="list"),
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
]

# Create your models here.
