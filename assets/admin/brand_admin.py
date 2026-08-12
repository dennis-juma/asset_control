from django.contrib import admin

from assets.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "country",
        "is_active",
        "created_at",
    )

    list_filter = (
        "country",
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
                    "country",
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