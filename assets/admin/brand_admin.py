from django.contrib import admin

from assets.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "company",
        "is_active",
        "created_at",
    )

    list_filter = (
        "company",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "description",
    )

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

    fieldsets = (
        (
            "Brand Information",
            {
                "fields": (
                    "company",
                    "code",
                    "name",
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