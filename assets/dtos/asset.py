from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from assets.models import AssetModel
from organizations.models import Company


@dataclass
class AssetCreateDTO:
    company: Company
    asset_model: AssetModel
    serial_number: str

    purchase_date: date | None = None
    received_date: date | None = None
    purchase_cost: Decimal | None = None
    invoice_number: str = ""

    condition: str = ""
    remarks: str = ""

@dataclass
class AssetUpdateDTO:
    company: Company
    asset_model: AssetModel
    serial_number: str

    purchase_date: date | None = None
    received_date: date | None = None
    purchase_cost: Decimal | None = None
    invoice_number: str = ""

    condition: str = ""
    remarks: str = ""

    is_active: bool = True