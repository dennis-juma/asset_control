from django.contrib import admin

from organizations.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "symbol",
        "is_default",
        "is_active",
    )
    search_fields = (
        "code",
        "name",
    )
    list_filter = (
        "is_default",
        "is_active",
    )