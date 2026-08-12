from dataclasses import dataclass
from datetime import date

from assets.models import Asset
from assets.models.asset_assignment import AssetAssignment
from employees.models import Employee
from organizations.models import Country, Site


@dataclass(slots=True)
class AssetTransferCreateDTO:
    """
    DTO used when transferring an asset.
    """

    country: Country

    asset: Asset

    previous_assignment: AssetAssignment | None = None

    to_employee: Employee | None = None

    to_site: Site | None = None

    transfer_date: date | None = None

    reason: str | None = None

    remarks: str | None = None


@dataclass(slots=True)
class AssetTransferUpdateDTO:
    """
    DTO used when updating transfer information.
    """

    transfer_date: date | None = None

    reason: str | None = None

    remarks: str | None = None

    is_active: bool = True