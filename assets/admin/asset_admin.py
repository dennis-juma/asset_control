from django.contrib import admin

from assets.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "asset_tag",
        "serial_number",
        "asset_model",
        "company",
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
        "company",
        "status",
        "condition",
        "is_active",
    )

    autocomplete_fields = (
        "company",
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