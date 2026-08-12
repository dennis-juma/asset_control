from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator


class Continent(models.TextChoices):
    AFRICA = "AFRICA", "Africa"
    ASIA = "ASIA", "Asia"
    EUROPE = "EUROPE", "Europe"
    NORTH_AMERICA = "NORTH_AMERICA", "North America"
    SOUTH_AMERICA = "SOUTH_AMERICA", "South America"
    OCEANIA = "OCEANIA", "Oceania"
    ANTARCTICA = "ANTARCTICA", "Antarctica"


class Country(BaseModel):
    """
    Master list of countries used throughout the system.

    Referenced by:
    - Country
    - Site
    - Employee
    - Vendor
    - Warehouse
    """

    slug_source = "name"

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    official_name = models.CharField(
        max_length=200,
        blank=True,
    )

    iso2 = models.CharField(
        max_length=2,
        unique=True,
    )

    iso3 = models.CharField(
        max_length=3,
        unique=True,
    )

    phone_code = models.CharField(
        max_length=10,
    )

    currency = models.CharField(
        max_length=10,
        default="TZS",
    )

    timezone = models.CharField(
        max_length=100,
        default="Africa/Dar_es_Salaam",
    )

    continent = models.CharField(
        max_length=20,
        choices=Continent.choices,
        default=Continent.AFRICA,
    )

    flag = models.ImageField(
        upload_to="countries/flags/",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.code:
            self.code = CodeGenerator.generate(
                Country,
                "CTR",
            )

        super().save(*args, **kwargs)