from dataclasses import dataclass
from datetime import date

from assets.models import Asset, AssetAssignment
from organizations.models import Company, Site
from employees.models import Employee
from assets.choices import AssignmentType


@dataclass
class AssetAssignmentCreateDTO:

    company: Company

    asset: Asset

    assignment_type: AssignmentType

    employee: Employee | None = None

    site: Site | None = None

    assigned_date: date | None = None

    expected_return_date: date | None = None

    remarks: str = ""


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