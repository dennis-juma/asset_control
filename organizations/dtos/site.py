from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from common.choices import SiteType


@dataclass(slots=True)
class SiteCreateDTO:

    country_id: UUID

    name: str

    site_type: SiteType

    email: str = ""

    phone: str = ""

    address: str = ""

    city: str = ""

    postal_code: str = ""

    latitude: Optional[Decimal] = None

    longitude: Optional[Decimal] = None

    description: str = ""


@dataclass(slots=True)
class SiteUpdateDTO:

    country_id: UUID

    name: str

    site_type: SiteType

    email: str = ""

    phone: str = ""

    address: str = ""

    city: str = ""

    postal_code: str = ""

    latitude: Optional[Decimal] = None

    longitude: Optional[Decimal] = None

    is_active: bool = True



@dataclass(slots=True)
class SiteDetailDTO:

    id: UUID

    code: str

    country: str

    name: str

    site_type: str

    email: str

    phone: str

    address: str

    city: str

    postal_code: str

    latitude: Optional[Decimal]

    longitude: Optional[Decimal]


    is_active: bool
