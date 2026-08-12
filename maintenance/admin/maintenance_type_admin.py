from django.contrib import admin

from maintenance.models import MaintenanceType


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "country",
        "is_active",
    )

    list_filter = (
        "country",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = (
        "name",
    )

    autocomplete_fields = (
        "country",
    )

    readonly_fields = (
        "code",
        "slug",
        "created_at",
        "updated_at",
    )