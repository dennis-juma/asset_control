from django.db import models

from core.models import BaseModel
from core.services import CodeGenerator
from organizations.models import Company


class JobTitle(BaseModel):
    """
    Master list of job titles within a company.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="job_titles",
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
        ordering = ["name"]
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_company_job_title",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.generate(
                JobTitle,
                prefix="JOB",
                digits=3,
            )

        super().save(*args, **kwargs)