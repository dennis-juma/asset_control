from django.contrib import admin

from assets.models import AssetCategory


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):

    
    list_display = (
        "name",
        "code",
        "company",
        "asset_type",
        "depreciable",
        "requires_assignment",
        "is_active",
    )

    list_filter = (
        "company",
        "asset_type",
        "depreciable",
        "requires_assignment",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    autocomplete_fields = (
        "company",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )
    readonly_fields = (
    "code",
    "slug",
    "created_at",
    "updated_at",
)