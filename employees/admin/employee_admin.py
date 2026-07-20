from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "full_name",
        "company",
        "department",
        "job_title",
        "site",
        "employment_status",
        "is_active",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "work_email",
    )

    list_filter = (
        "company",
        "department",
        "site",
        "employment_status",
        "employment_type",
        "is_active",
    )

    autocomplete_fields = (
        "user",
        "company",
        "department",
        "site",
        "job_title",
        "manager",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "company",
        "department",
        "first_name",
    )