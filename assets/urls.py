from django.urls import path

from assets.views.asset_list import AssetListView
from assets.views.transfer import AssetTransferView
from assets.views import (
    AssetCategoryCreateView,
    AssetCategoryDeleteView,
    AssetCategoryDetailView,
    AssetCategoryListView,
    AssetCategoryUpdateView,
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
]

# Create your models here.
