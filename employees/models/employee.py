from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from departments.models import Department
from job_titles.models import JobTitle
from organizations.models import Company
from sites.models import Site

from .choices import EmploymentStatus, EmploymentType


class Employee(BaseModel):

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Employee number issued by HR.",
    )

    first_name = models.CharField(max_length=100)

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(max_length=100)

    work_email = models.EmailField(
        unique=True,
    )

    personal_email = models.EmailField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="employees/photos/",
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
    )

    hire_date = models.DateField()

    termination_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"

    @property
    def full_name(self):
        return " ".join(
            filter(
                None,
                [
                    self.first_name,
                    self.middle_name,
                    self.last_name,
                ],
            )
        )

    def clean(self):
        errors = {}

        if self.department.company_id != self.company_id:
            errors["department"] = (
                "Department must belong to the selected company."
            )

        if self.job_title.company_id != self.company_id:
            errors["job_title"] = (
                "Job title must belong to the selected company."
            )

        if self.manager and self.manager == self:
            errors["manager"] = (
                "Employee cannot be their own manager."
            )

        if (
            self.termination_date
            and self.termination_date < self.hire_date
        ):
            errors["termination_date"] = (
                "Termination date cannot be before hire date."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)