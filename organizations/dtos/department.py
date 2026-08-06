from dataclasses import dataclass


@dataclass
class DepartmentCreateDTO:
    company: str
    site: str
    parent: str | None
    name: str
    cost_center: str
    description: str


@dataclass
class DepartmentUpdateDTO:
    company: str
    site: str
    parent: str | None
    name: str   
    cost_center: str
    description: str
    is_active: bool