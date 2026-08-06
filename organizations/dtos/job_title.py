from dataclasses import dataclass


@dataclass
class JobTitleCreateDTO:
    company: str
    department: str
    name: str
    description: str


@dataclass
class JobTitleUpdateDTO:
    company: str
    department: str
    name: str
    description: str
    is_active: bool