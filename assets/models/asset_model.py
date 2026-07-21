from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code

from organizations.models import Company

from .asset_category import AssetCategory
from .brand import Brand


class AssetModel(BaseModel):
    """
    Manufacturer's asset model.

    Examples:
        Dell Latitude 5440
        HP ProBook 440 G11
        Lenovo ThinkPad E16 Gen 2
        Zebra DS2208
    """

    slug_source = "name"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
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

    name = models.CharField(
        max_length=150,
        help_text="Manufacturer model name.",
    )

    code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
    )

    manufacturer_part_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Manufacturer Part Number (MPN)",
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["brand__name", "name"]

        verbose_name = "Asset Model"
        verbose_name_plural = "Asset Models"

        constraints = [
            models.UniqueConstraint(
                fields=["company", "brand", "name"],
                name="unique_asset_model_per_brand",
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_asset_model_code_per_company",
            ),
        ]

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["category"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def clean(self):
        super().clean()

        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({
                "name": "Model name cannot be empty."
            })

        if (
            self.category_id
            and self.category.company_id != self.company_id
        ):
            raise ValidationError({
                "category": "Category belongs to another company."
            })

        if (
            self.brand_id
            and self.brand.company_id != self.company_id
        ):
            raise ValidationError({
                "brand": "Brand belongs to another company."
            })

        if AssetModel.objects.filter(
            company=self.company,
            brand=self.brand,
            name__iexact=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": "This model already exists for the selected brand."
            })

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.name}"