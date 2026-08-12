from dataclasses import dataclass


@dataclass
class JobTitleCreateDTO:
    country: str
    department: str
    name: str
    description: str


@dataclass
class JobTitleUpdateDTO:
    country: str
    department: str
    name: str
    description: str
    is_active: bool