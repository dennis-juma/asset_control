from assets.choices import (
    AssetCondition,
    AssetStatus,
)
from assets.dtos import (
    AssetCreateDTO,
    AssetUpdateDTO,
)
from assets.models import Asset
from assets.repositories import AssetRepository
from assets.validators import AssetValidator


class AssetService:

    def __init__(self):
        self.repository = AssetRepository()
        self.validator = AssetValidator()

    # =====================================================
    # Create
    # =====================================================

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

        return self.repository.create(asset)

    # =====================================================
    # Update
    # =====================================================

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

        return self.repository.update(asset)

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        asset: Asset,
    ):

        self.repository.delete(asset)