from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "employee_id",
        "user_type",
        "is_active",
    )

    list_filter = (
        "user_type",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Company Information",
            {
                "fields": (
                    "employee_id",
                    "phone",
                    "profile_photo",
                    "user_type",
                )
            },
        ),
    )