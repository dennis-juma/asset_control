from django.db import transaction
from assets.choices import (
    AssetCondition,
    AssetStatus,
)
from assets.choices.history_choices import AssetHistoryEvent
from assets.dtos import (
    AssetCreateDTO,
    AssetUpdateDTO,
)
from assets.models import Asset
from assets.repositories import AssetRepository
from assets.validators import AssetValidator
from assets.services.asset_history_service import AssetHistoryService

class AssetService:

    def __init__(self):
        self.repository = AssetRepository()
        self.validator = AssetValidator()

    # =====================================================
    # Create
    # =====================================================
    @transaction.atomic
    def create(
        self,
        dto: AssetCreateDTO,
    ) -> Asset:

        self.validator.validate_create(dto)

        asset = Asset(
            company=dto.company,
            asset_model=dto.asset_model,
            serial_number=dto.serial_number,
            purchase_date=dto.purchase_date,
            received_date=dto.received_date,
            purchase_cost=dto.purchase_cost,
            invoice_number=dto.invoice_number,
            condition=dto.condition or AssetCondition.NEW,
            status=AssetStatus.AVAILABLE,
            remarks=dto.remarks,
        )
        asset = self.repository.create(asset)
        AssetHistoryService.log_event(
        asset=asset,
        event_type=AssetHistoryEvent.CREATED,
        new_status=AssetStatus.AVAILABLE,
        reference=str(asset.pk),
        notes="Asset created.",
    )

        return asset

    # =====================================================
    # Update
    # =====================================================
    @transaction.atomic
    def update(
    self,
    asset: Asset,
    dto: AssetUpdateDTO,
) -> Asset:

        self.validator.validate_update(
            asset,
            dto,
        )

        asset.company = dto.company
        asset.asset_model = dto.asset_model
        asset.serial_number = dto.serial_number
        asset.purchase_date = dto.purchase_date
        asset.received_date = dto.received_date
        asset.purchase_cost = dto.purchase_cost
        asset.invoice_number = dto.invoice_number
        asset.condition = dto.condition
        asset.remarks = dto.remarks
        asset.is_active = dto.is_active

        asset = self.repository.update(asset)

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.UPDATED,
            reference=str(asset.pk),
            notes="Asset information updated.",
            metadata={
                "asset_model_id": str(asset.asset_model_id)
                if asset.asset_model_id
                else None,
                "condition": asset.condition,
                "is_active": asset.is_active,
            },
        )

        return asset



    # =====================================================
    # Change Status
    # =====================================================
    @transaction.atomic
    def change_status(
        self,
        asset: Asset,
        new_status: str,
        performed_by=None,
        employee=None,
        site=None,
        reason: str = "",
        notes: str = "",
    ) -> Asset:

        old_status = asset.status

        # Nothing changed
        if old_status == new_status:
            return asset

        asset.status = new_status

        asset = self.repository.update(asset)

        AssetHistoryService.log_event(
            asset=asset,
            event_type=AssetHistoryEvent.STATUS_CHANGED,
            performed_by=performed_by,
            employee=employee,
            site=site,
            old_status=old_status,
            new_status=new_status,
            reference=str(asset.pk),
            notes=notes or reason or "Asset status changed.",
            metadata={
                "reason": reason,
            },
        )

        return asset



    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        asset: Asset,
    ):

        self.repository.delete(asset)