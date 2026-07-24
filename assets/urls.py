from django.urls import path

from assets.views.transfer import AssetTransferView

urlpatterns = [
    path(
        "transfer/<int:pk>/",
        AssetTransferView.as_view(),
        name="asset-transfer",
    ),
]

# Create your models here.
