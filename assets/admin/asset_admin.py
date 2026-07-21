from django.contrib import admin

from assets.models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "is_active",
    )