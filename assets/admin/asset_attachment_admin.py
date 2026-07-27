from django.contrib import admin

from assets.models import AssetAttachment


@admin.register(AssetAttachment)
class AssetAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "attachment_type",
        "original_filename",
        "created_by",
        "created_at",
    )

    list_filter = (
        "attachment_type",
        "created_at",
    )

    search_fields = (
        "asset__asset_code",
        "asset__serial_number",
        "original_filename",
    )

    autocomplete_fields = (
        "asset",
    )

    readonly_fields = (
        "original_filename",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    fieldsets = (
        (
            "Attachment Information",
            {
                "fields": (
                    "asset",
                    "attachment_type",
                    "file",
                    "description",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "original_filename",
                    "created_by",
                    "created_at",
                    "updated_by",
                    "updated_at",
                ),
            },
        ),
    )