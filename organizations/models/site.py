from django.db import models

from common.choices import SiteType
from core.models import BaseModel
from core.services import CodeGenerator
from .region import Region


class Site(BaseModel):
    slug_source = "name"
    """
    Physical office, warehouse, call center or AHQ.
    """

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="sites",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    site_type = models.CharField(
        max_length=3,
        choices=SiteType.choices,
    )

    address = models.TextField(blank=True)

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["region", "name"],
                name="unique_region_site",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_site_type_display()})"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Site,
                "SITE",
                digits=4,
            )
        super().save(*args, **kwargs)