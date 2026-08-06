from dataclasses import dataclass
from datetime import datetime
from django.core.files.uploadedfile import UploadedFile
from uuid import UUID

from organizations.models import Country


@dataclass(frozen=True, slots=True)
class CompanyDTO:
    id: UUID
    code: str
    name: str
    country_id: UUID
    country_name: str
    legal_name: str
    registration_number: str
    tax_number: str
    phone: str
    email: str
    website: str
    logo: str | None
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime



@dataclass(frozen=True, slots=True)
class CompanyCreateDTO:
    name: str
    country: Country
    legal_name: str = ""
    registration_number: str = ""
    tax_number: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    description: str = ""
    logo: UploadedFile | None = None


@dataclass(frozen=True, slots=True)
class CompanyUpdateDTO:
    name: str
    country: Country
    legal_name: str = ""
    registration_number: str = ""
    tax_number: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    description: str = ""
    logo: UploadedFile | None = None
