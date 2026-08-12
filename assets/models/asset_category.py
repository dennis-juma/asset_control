from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Country


class AssetCategory(BaseModel):
    """
    Classifies assets into business categories.

    Examples:
        IT Equipment
            â”œâ”€â”€ Laptop
            â”œâ”€â”€ Desktop
            â””â”€â”€ Printer

        Networking
            â”œâ”€â”€ Router
            â”œâ”€â”€ Switch
            â””â”€â”€ Firewall
    """

    slug_source = "name"

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="asset_categories",
        null=True,
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    description = models.TextField(
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            "sort_order",
            "name",
        ]

        verbose_name = "Asset Category"

        verbose_name_plural = "Asset Categories"

        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "country",
                    "parent",
                    "name",
                ],
                name="unique_asset_category_per_parent",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                AssetCategory,
                prefix="CAT",
                digits=3,
            )

        super().save(*args, **kwargs)
