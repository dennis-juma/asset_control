from django.contrib import admin

from organizations.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "company",
        "site",
        "cost_center",
        "is_active",
    )

    list_filter = (
        "company",
        "site",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "cost_center",
    )