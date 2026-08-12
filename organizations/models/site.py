from django.db import models

from common.choices import SiteType
from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models.country import Country



class Site(BaseModel):
    slug_source = "name"
    """
    Physical office, warehouse, call center or AHQ.
    """

    country = models.ForeignKey(
    Country,
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
        max_length=30,
        choices=SiteType.choices,
    )
    email = models.EmailField(
    blank=True,
)

    phone = models.CharField(
        max_length=30,
        blank=True,
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

    def __str__(self):
            return f"{self.name}"
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Site,
                prefix="SIT",
                digits=3,
            )

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_country_site",
            )
        ]
        verbose_name = "Site"
        verbose_name_plural = "Sites"
