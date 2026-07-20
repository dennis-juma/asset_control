from django.contrib import admin
from sites.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
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