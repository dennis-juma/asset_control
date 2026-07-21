from django.contrib import admin

from assets.models import AssetModel


@admin.register(AssetModel)
class AssetModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "brand",
        "category",
        "company",
        "is_active",
    )

    list_filter = (
        "company",
        "category",
        "brand",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "manufacturer_part_number",
        "brand__name",
        "category__name",
    )

    ordering = (
        "brand__name",
        "name",
    )

    readonly_fields = (
        "slug",
        "code",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    autocomplete_fields = (
        "company",
        "category",
        "brand",
    )

    list_select_related = (
        "company",
        "category",
        "brand",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "company",
                    "category",
                    "brand",
                    "name",
                    "manufacturer_part_number",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "code",
                    "slug",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                ),
            },
        ),
    )