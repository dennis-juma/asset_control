from django.contrib import admin

from organizations.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "country",
        "email",
        "country",
        "phone",
        "is_active",
        "country",
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

    autocomplete_fields = (
    "created_by",
    "updated_by",
)

    ordering = ("name",)
