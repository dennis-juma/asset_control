from dataclasses import dataclass

from organizations.models import Company
from assets.models import AssetCategory


@dataclass
class AssetCategoryCreateDTO:
    """
    Data Transfer Object for creating an Asset Category.
    """

    company: Company

    parent: AssetCategory | None

    name: str

    description: str = ""

    sort_order: int = 0


@dataclass
class AssetCategoryUpdateDTO:
    """
    Data Transfer Object for updating an Asset Category.
    """

    company: Company

    parent: AssetCategory | None

    name: str

    description: str = ""

    sort_order: int = 0

    is_active: bool = True