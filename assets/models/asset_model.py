from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Company

from assets.models import (
    AssetCategory,
    Brand,
)


class AssetModel(BaseModel):
    """
    Represents a product/model definition.

    Examples:
    - Dell Latitude 5420
    - HP LaserJet Pro M404dn
    - APC BX650LI
    """

    slug_source = "name"

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="asset_models",
    )

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.PROTECT,
        related_name="asset_models",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="asset_models",
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
    )

    manufacturer_part_number = models.CharField(
        max_length=100,
        blank=True,
    )

    technical_specifications = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = [
            "brand__name",
            "name",
        ]

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "brand",
                    "name",
                ],
                name="unique_asset_model_per_brand",
            ),
            models.UniqueConstraint(
                fields=[
                    "company",
                    "code",
                ],
                name="unique_asset_model_code_per_company",
            ),
        ]

        verbose_name = "Asset Model"
        verbose_name_plural = "Asset Models"

    def save(self, *args, **kwargs):

        if not self.code:

            self.code = CodeGenerator.generate(
                model=AssetModel,
                field="code",
                prefix="MOD",
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.brand.name} {self.name}"