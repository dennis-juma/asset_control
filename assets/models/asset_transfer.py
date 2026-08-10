from django.db import models

from assets.models import Asset
from assets.models.asset_assignment import AssetAssignment

from core.models import TransactionModel

from employees.models import Employee
from organizations.models import Company, Site


class AssetTransfer(TransactionModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="asset_transfers",
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="transfers",
    )

    previous_assignment = models.ForeignKey(
        AssetAssignment,
        on_delete=models.PROTECT,
        related_name="transfer_out",
    )

    new_assignment = models.ForeignKey(
        AssetAssignment,
        on_delete=models.PROTECT,
        related_name="transfer_in",
        null=True,
        blank=True,
    )

    from_employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_transfer_from_employee",
    )

    from_site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_transfer_from_site",
    )

    to_employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_transfer_to_employee",
    )

    to_site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asset_transfer_to_site",
    )

    transfer_date = models.DateField()

    reason = models.CharField(
        max_length=255,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-transfer_date"]
        verbose_name = "Asset Transfer"
        verbose_name_plural = "Asset Transfers"

    def __str__(self):
        return (
            f"{self.asset.asset_tag} "
            f"Transfer "
            f"{self.transfer_date}"
        )