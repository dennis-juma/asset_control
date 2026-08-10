from django.db import models
from assets.models import Asset
from core.models import TransactionModel
from organizations.models import Company,Site
from employees.models import Employee

from assets.choices import (
    AssignmentStatus,
    AssignmentType,
)



class AssetAssignment(TransactionModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="asset_assignments",
        null=True,
        blank=True
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="assignments",
        null=True,
        blank=True
    )
    assignment_type = models.CharField(
    max_length=20,
    choices=AssignmentType.choices,
    default=AssignmentType.EMPLOYEE,
    db_index=True,
)

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_assignments",
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_assignments",
    )

    assigned_date = models.DateField()

    expected_return_date = models.DateField(
        null=True,
        blank=True,
    )

    returned_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ACTIVE,
    )

    remarks = models.TextField(
        blank=True,
    )

    @property
    def assigned_to(self):
        if self.assignment_type == AssignmentType.EMPLOYEE:
            return self.employee

        if self.assignment_type == AssignmentType.SITE:
            return self.site

        return None


    @property
    def assigned_to_name(self):
        if self.assignment_type == AssignmentType.EMPLOYEE:
            if self.employee:
                return self.employee.full_name

            return "Unknown Employee"

        if self.assignment_type == AssignmentType.SITE:
            if self.site:
                return self.site.name

            return "Unknown Site"

        return "Unassigned"

    class Meta:
        ordering = ["-assigned_date"]
        verbose_name = "Asset Assignment"
        verbose_name_plural = "Asset Assignments"

    def __str__(self):
        if self.employee:
            return  (
        f"{self.asset.asset_tag} → "
        f"{self.assigned_to_name}"
    )

        return f"{self.asset.asset_tag} → {self.site}"