from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Company


class Brand(BaseModel):
    """
    Manufacturer or brand of an asset.

    Examples:
    - Dell
    - HP
    - Lenovo
    - Apple
    """

    slug_source = "name"

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="brands",
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=["company"],
            ),
            models.Index(
                fields=["code"],
            ),
            models.Index(
                fields=["name"],
            ),
            models.Index(
                fields=["is_active"],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_brand_name_per_company",
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_brand_code_per_company",
            ),
        ]

        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def save(self, *args, **kwargs):

        if not self.code:

            self.code = CodeGenerator.generate(
                model=Brand,
                 field_name="code",
                prefix="BRD",
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name