from django.contrib import admin

from organizations.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "iso2",
        "iso3",
        "currency",
        "continent",
        "is_active",
    )

    search_fields = (
        "name",
        "iso2",
        "iso3",
    )

    list_filter = (
        "continent",
        "is_active",
    )
