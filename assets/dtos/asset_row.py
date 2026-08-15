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

    country: Optional[str]
    category: Optional[str]
    brand: Optional[str]
    model: Optional[str]

    status: str
    condition: str

    purchase_date: Optional[date]
    received_date: Optional[date]
    purchase_cost: Optional[Decimal]
    invoice_number: str