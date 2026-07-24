from django.contrib import admin

from maintenance.models import MaintenanceType


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "company",
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

    ordering = (
        "name",
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