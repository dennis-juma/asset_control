# organizations/models/country.py

from django.db import models

from core.models import BaseModel
from .company import Company


class Country(BaseModel):
    """
    Countries where a company operates.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="countries",
    )

    name = models.CharField(
        max_length=100,
    )

    iso2 = models.CharField(
        max_length=2,
    )

    iso3 = models.CharField(
        max_length=3,
    )

    currency = models.CharField(
        max_length=10,
        default="TZS",
    )

    timezone = models.CharField(
        max_length=100,
        default="Africa/Dar_es_Salaam",
    )

    phone_code = models.CharField(
        max_length=10,
        default="+255",
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "iso2"],
                name="unique_company_country_iso2",
            ),
        ]

    def __str__(self):
        return self.name