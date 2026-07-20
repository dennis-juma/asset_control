from django.contrib import admin

from departments.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "company",
        "parent",
        "cost_center",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "cost_center",
    )

    list_filter = (
        "company",
        "is_active",
    )

    autocomplete_fields = (
        "company",
        "parent",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "company",
        "name",
    )