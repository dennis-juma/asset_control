from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from assets.choices.choices import AssignmentStatus
from assets.models.asset import Asset
from core.models import BaseModel
from employees.models import Employee


class AssetAssignment(BaseModel):
    """
    Represents the assignment of an asset to an employee.

    Business workflows such as assignment, return, transfer,
    asset status updates, and history logging are handled by
    AssetAssignmentService.
    """

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="assignments",
        db_index=True,
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="asset_assignments",
        db_index=True,
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="asset_assignments_created",
    )

    assigned_date = models.DateTimeField(
        default=timezone.now,
    )

    expected_return_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected date the asset should be returned.",
    )

    returned_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="asset_assignments_returned",
    )

    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ACTIVE,
        db_index=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-assigned_date"]
        verbose_name = "Asset Assignment"
        verbose_name_plural = "Asset Assignments"

        constraints = [
            models.UniqueConstraint(
                fields=["asset", "status"],
                condition=models.Q(status=AssignmentStatus.ACTIVE),
                name="unique_active_asset_assignment",
            ),
        ]

        indexes = [
            models.Index(fields=["employee", "status"]),
            models.Index(fields=["assigned_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.asset} → {self.employee}"

    def clean(self) -> None:
        """
        Validate assignment business rules.
        """
        super().clean()

        errors = {}

        # Prevent modification of returned assignments
        if self.pk:
            previous = AssetAssignment.objects.filter(pk=self.pk).first()

            if (
                previous
                and previous.status == AssignmentStatus.RETURNED
            ):
                raise ValidationError(
                    "Returned assignments cannot be modified."
                )

        # Only one active assignment per asset
        if self.status == AssignmentStatus.ACTIVE:
            active_assignment_exists = (
                AssetAssignment.objects.filter(
                    asset=self.asset,
                    status=AssignmentStatus.ACTIVE,
                )
                .exclude(pk=self.pk)
                .exists()
            )

            if active_assignment_exists:
                errors["asset"] = (
                    "This asset is already assigned to another employee."
                )

        # Returned date requires RETURNED status
        if (
            self.returned_date
            and self.status != AssignmentStatus.RETURNED
        ):
            errors["status"] = (
                "Returned assets must have status RETURNED."
            )

        # RETURNED status requires returned date
        if (
            self.status == AssignmentStatus.RETURNED
            and not self.returned_date
        ):
            errors["returned_date"] = (
                "Please provide the return date."
            )

        # Return date cannot precede assignment date
        if (
            self.assigned_date
            and self.returned_date
            and self.returned_date < self.assigned_date
        ):
            errors["returned_date"] = (
                "Return date cannot be before the assignment date."
            )

        # Expected return date validation
        if (
            self.assigned_date
            and self.expected_return_date
            and self.expected_return_date < self.assigned_date.date()
        ):
            errors["expected_return_date"] = (
                "Expected return date cannot be before the assignment date."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        """
        Validate and persist the assignment.

        Cross-model business logic such as asset status updates,
        history logging, notifications, and assignment workflows
        is handled by AssetAssignmentService.
        """
        self.full_clean()
        super().save(*args, **kwargs)