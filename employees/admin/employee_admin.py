from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "first_name",
        "last_name",
        "company",
        "department",
        "job_title",
        "is_active",
    )

    readonly_fields = ()

    ordering = (
        "employee_id",
    )

    list_filter = (
        "company",
        "site",
        "department",
        "job_title",
        "gender",
        "is_active",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "middle_name",
        "last_name",
        "email",
    )