from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Company


class Department(BaseModel):
    """
    Represents an organizational department.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="departments",
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
                fields=["company", "name"],
                name="unique_company_department",
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                Department,
                prefix="DEP",
                digits=3,
            )

        super().save(*args, **kwargs)