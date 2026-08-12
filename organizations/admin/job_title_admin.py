from django.contrib import admin

from organizations.models import JobTitle


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "country",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "country",
        "is_active",
    )

    autocomplete_fields = (
        "country",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "country",
        "name",
    )