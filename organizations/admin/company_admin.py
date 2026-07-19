from django.contrib import admin

from organizations.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "email",
        "phone",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "email",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = ("name",)