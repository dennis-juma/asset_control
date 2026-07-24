from django.db import models
from organizations.models import Company, Currency
from assets.models import AssetCategory, Brand, AssetModel, Vendor
from core.models import BaseModel
from django.utils import timezone
from assets.choices.choices import AssetStatus, AssetCondition
from django.core.exceptions import ValidationError
from assets.choices.history_choices import AssetHistoryEvent

class Asset(BaseModel):
    
    """
    Represents a physical company asset.
    """
    slug_source = "asset_tag"
    asset_tag = models.CharField(
    max_length=30,
    unique=True,
    help_text="Unique asset tag.",
)

    serial_number = models.CharField(
    max_length=150,
    blank=True,
    help_text="Manufacturer serial number.",
)

    barcode = models.CharField(
    max_length=150,
    help_text="Barcode value.",
    null=True,
    blank=True,
)
    company = models.ForeignKey(
    Company,
    on_delete=models.PROTECT,
    related_name="assets",
    null=True,
    blank=True,
)
    category = models.ForeignKey(
    AssetCategory,
    on_delete=models.PROTECT,
    related_name="assets",
    null=True,
    blank=True,
)
    brand = models.ForeignKey(
    Brand,
    on_delete=models.PROTECT,
    related_name="assets",
    null=True,
    blank=True,
)
    model = models.ForeignKey(
    AssetModel,
    on_delete=models.PROTECT,
    related_name="assets",
    null=True,
    blank=True,
)
    vendor = models.ForeignKey(
    Vendor,
    on_delete=models.PROTECT,
    related_name="assets",
    blank=True,
    null=True,
)
    currency = models.ForeignKey(
    Currency,
    on_delete=models.PROTECT,
    related_name="assets",
    blank=True,
    null=True,
)
    purchase_date = models.DateField(
    null=True,
    blank=True,
)

    purchase_price = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True,
)
    
    



    invoice_number = models.CharField(
    max_length=100,
    blank=True,
)

    po_number = models.CharField(
    max_length=100,
    blank=True,
)
    
    # ==========================
# Warranty Information
# ==========================

    warranty_start = models.DateField(
    null=True,
    blank=True,
)

    warranty_end = models.DateField(
    null=True,
    blank=True,
)
    # ==========================
# Status Information
# ==========================

    status = models.CharField(
    max_length=20,
    choices=AssetStatus.choices,
    default=AssetStatus.IN_STOCK,
)

    condition = models.CharField(
    max_length=20,
    choices=AssetCondition.choices,
    default=AssetCondition.NEW,
)
    @property
    def is_under_warranty(self):
        if not self.warranty_end:
            return False
        return self.warranty_end >= timezone.now().date()

    def clean(self):
        super().clean()

        errors = {}

        if (
            self.warranty_start
            and self.warranty_end
            and self.warranty_end < self.warranty_start
        ):
            errors["warranty_end"] = (
                "Warranty end date cannot be before warranty start date."
            )

        if (
            self.purchase_price is not None
            and self.purchase_price < 0
        ):
            errors["purchase_price"] = (
                "Purchase price cannot be negative."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.asset_tag]

        if self.model:
            parts.append(str(self.model))

        return " - ".join(parts)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ["-created_at"]


    def log_history(
        self,
        *,
        event_type,
        performed_by=None,
        employee=None,
        site=None,
        old_status=None,
        new_status=None,
        reference="",
        notes="",
        metadata=None,
    ):
        """
        Record an asset history event.
        """

        AssetHistoryService.log_event(
            asset=self,
            event_type=event_type,
            performed_by=performed_by,
            employee=employee,
            site=site,
            old_status=old_status,
            new_status=new_status,
            reference=reference,
            notes=notes,
            metadata=metadata,
        )