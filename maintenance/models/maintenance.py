from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from core.models import BaseModel
from core.services.code_generator import CodeGenerator
from organizations.models import Company, Currency

from assets.models import Asset, Vendor

from .maintenance_type import MaintenanceType
from maintenance.choices import (
    MaintenanceStatus,
    MaintenancePriority,
)


class Maintenance(BaseModel):
    """
    Records all maintenance activities performed on an asset.
    """

    slug_source = None

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="maintenances",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="maintenances",
    )

    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name="maintenances",
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name="maintenances",
        null=True,
        blank=True,
    )

    reference = models.CharField(
    max_length=20,
    unique=True,
    editable=False,
    db_index=True,
)
    estimated_completion_date = models.DateField(
    null=True,
    blank=True,
)
    previous_asset_status = models.CharField(
    max_length=20,
    blank=True,
    editable=False,
)
    
    # =====================================
    # Workflow
    # =====================================

    status = models.CharField(
        max_length=20,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.SCHEDULED,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=MaintenancePriority.choices,
        default=MaintenancePriority.MEDIUM,
        db_index=True,
    )


    # =====================================
    # Scheduling
    # =====================================

    scheduled_date = models.DateField()

    started_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    next_maintenance_date = models.DateField(
        null=True,
        blank=True,
    )

    # =====================================
    # Financial Information
    # =====================================

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="maintenances",
        null=True,
        blank=True,
    )

    # =====================================
    # Warranty
    # =====================================

    under_warranty = models.BooleanField(
        default=False,
    )

    warranty_claim_number = models.CharField(
        max_length=100,
        blank=True,
    )

    # =====================================
    # Technician
    # =====================================

    technician = models.CharField(
        max_length=150,
        blank=True,
    )

    # =====================================
    # Description
    # =====================================

    description = models.TextField()


    resolution = models.TextField(
        blank=True,
    )


    class Meta:
        ordering = ["-scheduled_date", "-created_at"]

        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenance"

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["asset"]),
            models.Index(fields=["maintenance_type"]),
            models.Index(fields=["vendor"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["scheduled_date"]),
            
        ]

    def clean(self):
        super().clean()

        errors = {}

        # Company consistency
        if (
            self.asset_id
            and self.asset.company_id != self.company_id
        ):
            errors["asset"] = (
                "Asset belongs to another company."
            )

        if (
            self.vendor_id
            and self.vendor.company_id != self.company_id
        ):
            errors["vendor"] = (
                "Vendor belongs to another company."
            )

        if (
            self.maintenance_type_id
            and self.maintenance_type.company_id != self.company_id
        ):
            errors["maintenance_type"] = (
                "Maintenance Type belongs to another company."
            )

        # Cost validation
        if self.cost < 0:
            errors["cost"] = (
                "Maintenance cost cannot be negative."
            )

        # Date validations
        if (
            self.started_date
            and self.started_date.date() < self.scheduled_date
        ):
            errors["started_date"] = (
                "Started date cannot be before scheduled date."
            )

        if (
            self.completed_date
            and self.started_date
            and self.completed_date < self.started_date
        ):
            errors["completed_date"] = (
                "Completed date cannot be before started date."
            )

        if (
            self.status == MaintenanceStatus.COMPLETED
            and not self.completed_date
        ):
            errors["completed_date"] = (
                "Completed maintenance requires a completion date."
            )

        if (
            self.status == MaintenanceStatus.CANCELLED
            and self.completed_date
        ):
            errors["completed_date"] = (
                "Cancelled maintenance cannot have a completion date."
            )

        if (
            self.next_maintenance_date
            and self.completed_date
            and self.next_maintenance_date < self.completed_date.date()
        ):
            errors["next_maintenance_date"] = (
                "Next maintenance date cannot be before completion."
            )
        
        if (
        self.currency_id
        and self.currency.company_id != self.company_id
    ):
            errors["currency"] = (
            "Currency belongs to another company."
        )
        if not self.description.strip():
                errors["description"] = (
                    "Description cannot be empty."
                )
        if (
        self.warranty_claim_number
    and not self.under_warranty
):
            errors["warranty_claim_number"] = (
        "Warranty claim number requires the asset to be under warranty."
    )

        if errors:
            raise ValidationError(errors)
        
    def __str__(self):
        return (
            f"{self.reference} - "
            f"{self.asset.asset_tag}"
        )
    
    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.reference:
            self.reference = CodeGenerator.generate(
                model=Maintenance,
                field="reference",
                prefix="MNT",
                digits=6,
            )

        super().save(*args, **kwargs)



    @transaction.atomic
    def start(self):
        """
        Start maintenance.
        """
        self.previous_asset_status = self.asset.status

        if self.status != MaintenanceStatus.SCHEDULED:
            raise ValidationError(
                "Only scheduled maintenance can be started."
            )

        self.status = MaintenanceStatus.IN_PROGRESS
        self.started_date = timezone.now()

        # Update asset status
        self.asset.status = Asset.AssetStatus.MAINTENANCE
        self.asset.save(update_fields=["status", "updated_at"])

        self.save()

    @transaction.atomic
    def complete(self, resolution=""):
        """
        Complete maintenance.
        """

        if self.status != MaintenanceStatus.IN_PROGRESS:
            raise ValidationError(
                "Only maintenance in progress can be completed."
            )

        self.status = MaintenanceStatus.COMPLETED
        self.completed_date = timezone.now()

        if resolution:
            self.resolution = resolution

        # Return asset to available
        self.asset.status = (
            self.previous_asset_status or
            Asset.AssetStatus.AVAILABLE)
        self.asset.save(update_fields=["status", "updated_at"])

        self.save()

    @transaction.atomic
    def cancel(self, reason=""):
        """
        Cancel maintenance.
        """

        if self.status == MaintenanceStatus.COMPLETED:

            raise ValidationError(
                "Completed maintenance cannot be cancelled."
            )

        self.status = MaintenanceStatus.CANCELLED

        if reason:
            self.resolution = reason

        # Restore asset if maintenance had started
        if self.started_date:
            self.asset.status = (
                self.previous_asset_status or
                Asset.AssetStatus.AVAILABLE
            )
            self.asset.save(update_fields=["status", "updated_at"])

        self.save()