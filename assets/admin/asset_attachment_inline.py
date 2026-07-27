from django.contrib import admin

from assets.models import AssetAttachment


class AssetAttachmentInline(admin.TabularInline):
    model = AssetAttachment

    extra = 1

    fields = (
        "attachment_type",
        "file",
        "original_filename",
        "description",
    )

    readonly_fields = (
        "original_filename",
    )

    autocomplete_fields = (
        "asset",
    )