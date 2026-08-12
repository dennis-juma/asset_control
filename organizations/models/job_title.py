from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import (
    Country,
    Department,
)


class JobTitle(BaseModel):
    """
    Master list of job titles within a department.
    """

    slug_source = "name"

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="job_titles",
        null=True,
        blank=True,
        
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="job_titles",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["department", "name"]

        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "country",
                    "department",
                    "name",
                ],
                name="unique_department_job_title",
            ),
        ]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                JobTitle,
                prefix="JOB",
                digits=3,
            )

        super().save(*args, **kwargs)