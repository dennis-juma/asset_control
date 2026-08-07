from dataclasses import dataclass


from organizations.models import Company


@dataclass
class BrandCreateDTO:
    """
    Data Transfer Object for creating a Brand.
    """

    company: Company

    name: str

    description: str = ""


@dataclass
class BrandUpdateDTO:
    """
    Data Transfer Object for updating a Brand.
    """

    company: Company

    name: str

    description: str = ""

    is_active: bool = True