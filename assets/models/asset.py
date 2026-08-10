from django.db import models
from organizations.models import Company
from assets.choices import (
    AssetCondition,
    AssetStatus,
)
from .asset_model import AssetModel
from core.models import BaseModel
from core.services import CodeGenerator


class Asset(BaseModel):
    """
    Represents one physical serialized asset.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="assets",
        null=True,
        blank=True,
    )

    asset_model = models.ForeignKey(
        AssetModel,
        on_delete=models.PROTECT,
        related_name="assets",
        null=True,
        blank=True,
    )

    asset_tag = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    serial_number = models.CharField(
        max_length=150,
        unique=True,
    )

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    received_date = models.DateField(
    null=True,
    blank=True,
    help_text="Date the asset was physically received.",
)

    purchase_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=AssetStatus.choices,
        default=AssetStatus.AVAILABLE,
    )

    condition = models.CharField(
        max_length=30,
        choices=AssetCondition.choices,
        default=AssetCondition.NEW,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "asset_tag",
        ]

        indexes = [
            models.Index(fields=["asset_tag"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["condition"]),
        ]

        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def save(self, *args, **kwargs):

        if not self.asset_tag:
            self.asset_tag = CodeGenerator.generate(
                model=Asset,
                prefix="AST",
                field_name="asset_tag",
                digits=6,
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset_tag} - {self.serial_number}"