from django.contrib import admin

from assets.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "company",
        "website",
        "is_active",
    )

    list_filter = (
        "company",
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
        "code",
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )