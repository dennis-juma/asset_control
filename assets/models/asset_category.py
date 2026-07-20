from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code
from organizations.models import Company

from .choices import AssetType


class AssetCategory(BaseModel):
    """
    Defines the classification of assets.

    Examples:
        - Laptop
        - Desktop
        - Printer
        - Router
        - UPS
        - Scanner
        - Headset
    """

    slug_source = "name"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="asset_categories",
    )

    name = models.CharField(
        max_length=100,
        help_text="Asset category name (e.g. Laptop, Printer).",
    )

    code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        help_text="Automatically generated category code.",
    )

    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        default=AssetType.PHYSICAL,
    )

    description = models.TextField(
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bootstrap or Font Awesome icon class.",
    )

    depreciable = models.BooleanField(
        default=True,
        help_text="Indicates whether the asset is depreciable.",
    )

    requires_serial_number = models.BooleanField(
        default=True,
        help_text="Require a serial number when creating an asset.",
    )

    requires_assignment = models.BooleanField(
        default=True,
        help_text="Require the asset to be assigned to an employee.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_asset_category_name_per_company",
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_asset_category_code_per_company",
            ),
        ]

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def clean(self):
        """
        Validate business rules.
        """
        super().clean()

        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({
                "name": "Category name cannot be empty."
            })

        if AssetCategory.objects.filter(
            company=self.company,
            name__iexact=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": "An asset category with this name already exists for this company."
            })

    def save(self, *args, **kwargs):
        """
        Automatically generate a category code.
        """
        if not self.code:
            self.code = generate_code(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company} - {self.name}"