from django.contrib import admin

from job_titles.models import JobTitle


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "company",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "company",
        "is_active",
    )

    autocomplete_fields = (
        "company",
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