# organizations/models/company.py

from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator


class Company(BaseModel):
    slug_source = "name"
    """
    Represents a legal company within the platform.
    Example:
        - Sun King Tanzania Ltd
        - Sun King Kenya Ltd
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    legal_name = models.CharField(
        max_length=200,
        blank=True,
    )

    registration_number = models.CharField(
        max_length=100,
        blank=True,
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(blank=True)

    logo = models.ImageField(
        upload_to="companies/logos/",
        blank=True,
        null=True,
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Company,
                "CMP",
            )
        super().save(*args, **kwargs)