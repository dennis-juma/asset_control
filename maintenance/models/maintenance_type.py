from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code
from organizations.models import Country


class MaintenanceType(BaseModel):
    """
    Master list of maintenance types.

    Examples:
        - Preventive Maintenance
        - Corrective Maintenance
        - Warranty Repair
        - Upgrade
        - Inspection
        - Cleaning
    """

    slug_source = "name"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="maintenance_types",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Maintenance Type"
        verbose_name_plural = "Maintenance Types"

        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_maintenance_type_name_per_country",
            ),
            models.UniqueConstraint(
                fields=["country", "code"],
                name="unique_maintenance_type_code_per_country",
            ),
        ]

        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def clean(self):
        super().clean()

        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({
                "name": "Maintenance type name cannot be empty."
            })

        if MaintenanceType.objects.filter(
            country=self.country,
            name__iexact=self.name,
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                "name": (
                    "A maintenance type with this name "
                    "already exists for this country."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.code:
            self.code = generate_code(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
