from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CountryCreateDTO:
    """
    DTO used when creating a country.
    """

    name: str

    official_name: str = ""

    iso2: str = ""

    iso3: str = ""

    phone_code: str = ""

    currency: str = "TZS"

    timezone: str = "Africa/Dar_es_Salaam"

    continent: str = "AFRICA"

    description: str = ""


@dataclass(slots=True, frozen=True)
class CountryUpdateDTO:
    """
    DTO used when updating a country.
    """

    name: str

    official_name: str = ""

    iso2: str = ""

    iso3: str = ""

    phone_code: str = ""

    currency: str = "TZS"

    timezone: str = "Africa/Dar_es_Salaam"

    continent: str = "AFRICA"

    description: str = ""

    is_active: bool = True


@dataclass(slots=True, frozen=True)
class CountryDetailDTO:
    """
    DTO used for displaying country details.
    """

    id: str

    code: str

    name: str

    official_name: str

    iso2: str

    iso3: str

    phone_code: str

    currency: str

    timezone: str

    continent: str

    description: str

    is_active: bool