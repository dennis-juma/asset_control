from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CompanyListDTO:
    id: UUID
    code: str
    name: str
    phone: str
    email: str
    is_default: bool
    is_active: bool
