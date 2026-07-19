from django.contrib import admin

from organizations.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "iso2",
        "currency",
    )

    search_fields = (
        "name",
        "iso2",
    )

    list_filter = (
        "company",
    )