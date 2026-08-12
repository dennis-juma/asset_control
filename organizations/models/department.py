from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Country, Site


class Department(BaseModel):
    """
    Represents an organizational department within a country and site.
    Supports hierarchical departments and cost center mapping.
    """

    slug_source = "name"

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="departments",
        null=True,
        blank=True,
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="departments",
        null=True,
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    cost_center = models.CharField(
        max_length=30,
        blank=True,
        help_text="Finance/ERP cost center code.",
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Department"
        verbose_name_plural = "Departments"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "country",
                    "site",
                    "name",
                ],
                name="unique_department_per_site",
            ),
        ]

        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["site"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Department,
                prefix="DEP",
                digits=4,
            )

        super().save(*args, **kwargs)