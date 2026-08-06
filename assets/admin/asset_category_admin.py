from django.contrib import admin

from assets.models import AssetCategory


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "parent",
        "company",
        "is_active",
    )

    list_filter = (
        "company",
        "parent",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "sort_order",
        "name",
    )

    readonly_fields = (
        "code",
        "slug",
        "created_at",
        "updated_at",
    )