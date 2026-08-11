from django.conf import settings
from django.db import models

from core.models import BaseModel

from organizations.models import Company, Site
from employees.models import Employee

from assets.models.asset import Asset
from assets.choices.choices import AssetStatus
from assets.choices.history_choices import AssetHistoryEvent


class AssetHistory(BaseModel):
    """
    Stores the lifecycle history of an asset.

    Records every significant event such as creation, assignment,
    return, maintenance, and status changes.
    """
    slug_source = "id"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="asset_histories",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="history",
    )

    event_type = models.CharField(
        max_length=40,
        choices=AssetHistoryEvent.choices,
    )

    event_date = models.DateTimeField(auto_now_add=True)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="performed_asset_history",
    )

    employee = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="asset_history",
    )

    site = models.ForeignKey(
        Site,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    old_status = models.CharField(
        max_length=30,
        choices=AssetStatus.choices,
        blank=True,
    )

    new_status = models.CharField(
        max_length=30,
        choices=AssetStatus.choices,
        blank=True,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Assignment No, Maintenance Ref, etc.",
    )

    notes = models.TextField(blank=True)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["-event_date"]

        verbose_name = "Asset History"

        verbose_name_plural = "Asset History"

        indexes = [
            models.Index(fields=["asset"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["event_date"]),
        ]

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.get_event_type_display()}"