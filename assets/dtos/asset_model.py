from dataclasses import dataclass

from organizations.models import Country

from assets.models import (
    AssetCategory,
    Brand,
)


@dataclass
class AssetModelCreateDTO:
    """
    Data Transfer Object for creating an Asset Model.
    """

    country: Country

    category: AssetCategory

    brand: Brand

    name: str

    manufacturer_part_number: str = ""

    technical_specifications: str = ""

    description: str = ""


@dataclass
class AssetModelUpdateDTO:
    """
    Data Transfer Object for updating an Asset Model.
    """

    country: Country

    category: AssetCategory

    brand: Brand

    name: str

    manufacturer_part_number: str = ""

    technical_specifications: str = ""

    description: str = ""

    is_active: bool = True