from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Country


class Region(BaseModel):
    """
    Administrative region within a country.
    Example:
        Arusha
        Mwanza
        Dodoma
    """

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="regions",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_country_region",
            )
        ]

    def __str__(self):
        return f"{self.country.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Region,
                "REG",
                digits=3,
            )
        super().save(*args, **kwargs)