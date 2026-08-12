from django.contrib import admin

from assets.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "asset_tag",
        "serial_number",
        "asset_model",
        "country",
        "status",
        "condition",
        "is_active",
    )

    search_fields = (
        "asset_tag",
        "serial_number",
        "asset_model__name",
        "asset_model__brand__name",
    )

    list_filter = (
        "country",
        "status",
        "condition",
        "is_active",
    )

    autocomplete_fields = (
        "country",
        "asset_model",
    )

    readonly_fields = (
        "asset_tag",
        "created_at",
        "updated_at",
    )

    ordering = (
        "asset_tag",
    )