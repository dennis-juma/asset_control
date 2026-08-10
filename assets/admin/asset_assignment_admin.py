from django.contrib import admin

from assets.models import AssetAssignment


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "employee",
        "site",
        "assigned_date",
        "returned_date",
        "status",
        "is_active",
    )

    search_fields = (
        "asset__asset_tag",
        "asset__serial_number",
        "employee__employee_id",
        "employee__first_name",
        "employee__last_name",
        "site__name",
    )

    list_filter = (
        "status",
        "company",
        "assigned_date",
        "returned_date",
        "is_active",
    )

    autocomplete_fields = (
        "company",
        "asset",
        "employee",
        "site",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-assigned_date",
    )

    list_select_related = (
        "company",
        "asset",
        "employee",
        "site",
    )