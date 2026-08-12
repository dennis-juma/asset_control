from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code
from organizations.models import Country

from .choices import VendorType


class Vendor(BaseModel):
    """
    Vendor master data.

    Examples:
        - Techno Brain Tanzania
        - Sahara Computers
        - Red Dot Distribution
        - Zebra Technologies
    """

    slug_source = "name"

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="vendors",
        null=True,
        blank=True,
    )

    vendor_type = models.CharField(
        max_length=30,
        choices=VendorType.choices,
        default=VendorType.SUPPLIER,
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
    )

    contact_person = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    tin = models.CharField(
        max_length=50,
        blank=True,
        help_text="Taxpayer Identification Number",
    )

    vrn = models.CharField(
        max_length=50,
        blank=True,
        help_text="VAT Registration Number",
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_vendor_name_per_country",
            ),
            models.UniqueConstraint(
                fields=["country", "code"],
                name="unique_vendor_code_per_country",
            ),
        ]

        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["vendor_type"]),
        ]

    def clean(self):
        super().clean()

        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({
                "name": "Vendor name cannot be empty."
            })

        if Vendor.objects.filter(
            country=self.country,
            name__iexact=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": "A vendor with this name already exists for this country."
            })

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = generate_code(self.name)
            code = base_code
            counter = 1

            while Vendor.objects.filter(
                country=self.country,
                code=code,
            ).exclude(pk=self.pk).exists():
                code = f"{base_code}{counter}"
                counter += 1

            self.code = code

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.country} - {self.name}"
