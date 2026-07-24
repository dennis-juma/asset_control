from django.contrib import admin

from assets.models import AssetAssignment


class AssetAssignmentInline(admin.TabularInline):
    model = AssetAssignment

    extra = 0

    can_delete = False

    fields = (
        "employee",
        "status",
        "assigned_date",
        "returned_date",
    )

    readonly_fields = (
        "employee",
        "status",
        "assigned_date",
        "returned_date",
    )

    ordering = (
        "-assigned_date",
    )

    show_change_link = True