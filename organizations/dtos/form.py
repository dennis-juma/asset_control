from dataclasses import dataclass


@dataclass
class DepartmentCreateDTO:
    country: str
    site: str
    parent: str | None
    name: str
    cost_center: str
    description: str


@dataclass
class DepartmentUpdateDTO:
    country: str
    site: str
    parent: str | None
    name: str   
    cost_center: str
    description: str
    is_active: bool