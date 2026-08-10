from django.contrib import admin

from assets.models import AssetTransfer


@admin.register(AssetTransfer)
class AssetTransferAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "from_employee",
        "to_employee",
        "transfer_date",
    )

    search_fields = (
        "asset__asset_tag",
    )

    list_filter = (
        "transfer_date",
    )