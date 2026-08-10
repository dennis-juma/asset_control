from dataclasses import dataclass
from datetime import date

from assets.models import Asset,AssetAssignment
from organizations.models import Company, Site
from employees.models import Employee
from assets.choices import AssignmentType


@dataclass
class AssetAssignmentCreateDTO:

    company: Company

    asset: Asset

    previous_assignment: AssetAssignment | None = None

    to_employee: Employee | None = None

    to_site: Site | None = None

    transfer_date: date | None = None

    reason: str | None = None

    remarks: str | None = None




@dataclass
class AssetAssignmentUpdateDTO:

    assignment_type: AssignmentType

    employee: Employee | None = None

    site: Site | None = None

    assigned_date: date | None = None

    expected_return_date: date | None = None

    remarks: str = ""

    is_active: bool = True


@dataclass
class AssetReturnDTO:

    returned_date: date

    remarks: str = ""