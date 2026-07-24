from django.contrib import admin
from organizations.models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "region",
        "site_type",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "region",
        "site_type",
        "is_active",
    )