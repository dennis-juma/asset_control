from django.contrib import admin

from assets.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "vendor_type",
        "company",
        "country",
        "contact_person",
        "phone",
        "email",
        "is_active",
    )

    list_filter = (
        "company",
        "country",
        "vendor_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "contact_person",
        "email",
        "phone",
        "tin",
        "vrn",
    )

    autocomplete_fields = (
        "company",
        "country",
    )

    readonly_fields = (
        "code",
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )