from django.db import models

from core.models import BaseModel
from core.utils.code import generate_code
from organizations.models import Company


class AssetStatus(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="asset_statuses",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
    )

    color = models.CharField(
        max_length=30,
        default="secondary",
        help_text="Bootstrap badge color",
    )

    description = models.TextField(
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            "sort_order",
            "name",
        ]
        verbose_name = "Asset Status"
        verbose_name_plural = "Asset Statuses"

    def save(self, *args, **kwargs):

        if not self.code:
            self.code = generate_code.generate(
                model=AssetStatus,
                prefix="STS",
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name