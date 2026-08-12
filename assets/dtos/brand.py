from dataclasses import dataclass


from organizations.models import Country


@dataclass
class BrandCreateDTO:
    """
    Data Transfer Object for creating a Brand.
    """

    country: Country

    name: str

    description: str = ""


@dataclass
class BrandUpdateDTO:
    """
    Data Transfer Object for updating a Brand.
    """

    country: Country

    name: str

    description: str = ""

    is_active: bool = True