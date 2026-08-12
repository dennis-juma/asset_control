from django.contrib import admin

from assets.models import AssetModel


@admin.register(AssetModel)
class AssetModelAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "brand",
        "name",
        "category",
        "country",
        "is_active",
        "created_at",
    )

    list_filter = (
        "country",
        "category",
        "brand",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "manufacturer_part_number",
        "brand__name",
        "category__name",
    )

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )

    ordering = (
        "brand",
        "name",
    )

    fieldsets = (
        (
            "Asset Model Information",
            {
                "fields": (
                    "country",
                    "category",
                    "brand",
                    "code",
                    "name",
                    "manufacturer_part_number",
                    "technical_specifications",
                    "description",
                ),
            },
        ),
        (
            "System",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )