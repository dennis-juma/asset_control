from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_number",
        "first_name",
        "last_name",
        "email",
        "department",
        "job_title",
        "site",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "department",
        "job_title",
        "site",
        "is_active",
    )

    search_fields = (
        "employee_number",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("employee_number",)

    autocomplete_fields = (
        "company",
        "department",
        "job_title",
        "site",
        "manager",
    )

    readonly_fields = (
        "employee_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Employee Information", {
            "fields": (
                "employee_number",
                "company",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "date_of_birth",
                "hire_date",
                "status",
            )
        }),
        ("Organization", {
            "fields": (
                "department",
                "job_title",
                "site",
                "manager",
            )
        }),
        ("Contact", {
            "fields": (
                "email",
                "phone",
            )
        }),
        ("Other", {
            "fields": (
                "profile_photo",
                "notes",
            )
        }),
        ("Audit", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )