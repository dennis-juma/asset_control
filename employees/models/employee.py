from django.conf import settings
from django.db import models

from common.choices import (
    Gender,
    SiteType,
)
from core.models import BaseModel
from organizations.models import (
    Company,
    Department,
    JobTitle,
    Site,
)


class Employee(BaseModel):
    """
    Employee master record.
    Used for asset assignment and employee management.
    """

    slug_source = "full_name"

    # =====================================================
    # Organization Information
    # =====================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    department = models.ForeignKey(
        Department,
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
        on_delete=models.PROTECT,
        related_name="team_members",
        null=True,
        blank=True,
    )

    # =====================================================
    # Employee Information
    # =====================================================

    employee_id = models.CharField(
        max_length=30,
        unique=True,
        help_text="Employee ID provided by HR.",
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    joining_date = models.DateField()

    last_working_date = models.DateField(
        null=True,
        blank=True,
        help_text="Employee's final working day.",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    photo = models.ImageField(
        upload_to="employees/photos/",
        null=True,
        blank=True,
    )

    # =====================================================
    # System Information
    # =====================================================

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="employee",
        null=True,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "first_name",
            "last_name",
        ]

        verbose_name = "Employee"
        verbose_name_plural = "Employees"

        constraints = [
            models.UniqueConstraint(
                fields=["company", "employee_id"],
                name="unique_company_employee_id",
            ),
        ]

        indexes = [
            models.Index(fields=["employee_id"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["company"]),
            models.Index(fields=["site"]),
            models.Index(fields=["department"]),
            models.Index(fields=["job_title"]),
        ]

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

    @property
    def is_current_employee(self):
        """
        Returns True if the employee is currently employed.
        """
        return (
            self.is_active and
            self.last_working_date is None
        )

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"