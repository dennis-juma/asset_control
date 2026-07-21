from django.db import models

from core.models import BaseModel


class Currency(BaseModel):
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text="ISO 4217 currency code (e.g. TZS, USD).",
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    symbol = models.CharField(
        max_length=10,
        blank=True,
    )

    decimal_places = models.PositiveSmallIntegerField(
        default=2,
    )

    is_default = models.BooleanField(
        default=False,
        help_text="Default currency used by the system.",
    )

    class Meta:
        ordering = ["code"]
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.code} - {self.name}"