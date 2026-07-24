from django.contrib import admin

from assets.models import AssetHistory


@admin.register(AssetHistory)
class AssetHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "event_type",
        "performed_by",
        "event_date",
        "new_status",
    )

    list_filter = (
        "event_type",
        "new_status",
        "event_date",
    )

    search_fields = (
        "asset__asset_tag",
        "reference",
        "notes",
    )

    autocomplete_fields = (
        "asset",
        "performed_by",
        "employee",
    )

    readonly_fields = (
        "event_date",
    )

    ordering = (
        "-event_date",
    )

    list_per_page = 25