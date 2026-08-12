from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AssetRowDTO:
    """
    Represents a single asset displayed in the asset list.
    """

    id: UUID

    asset_tag: str
    serial_number: str
    barcode: Optional[str]

    country: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    vendor: Optional[str]

    status: str
    condition: str

    purchase_date: Optional[date]
    purchase_price: Optional[Decimal]


    under_warranty: bool