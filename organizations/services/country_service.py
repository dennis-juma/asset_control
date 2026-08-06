from organizations.dtos import (
    CountryCreateDTO,
    CountryUpdateDTO,
)

from organizations.models import Country
from organizations.repositories import CountryRepository


class CountryService:
    """
    Business logic for Country.
    """

    def __init__(self):
        self.repository = CountryRepository()

    def create_country(
        self,
        dto: CountryCreateDTO,
    ) -> Country:

        name = dto.name.strip()
        iso2 = dto.iso2.upper().strip()
        iso3 = dto.iso3.upper().strip()

        if self.repository.exists(name=name):
            raise ValueError(
                "A country with this name already exists."
            )

        if self.repository.exists(iso2=iso2):
            raise ValueError(
                "ISO2 code already exists."
            )

        if self.repository.exists(iso3=iso3):
            raise ValueError(
                "ISO3 code already exists."
            )

        return self.repository.create(
            name=name,
            official_name=dto.official_name.strip(),
            iso2=iso2,
            iso3=iso3,
            phone_code=dto.phone_code.strip(),
            currency=dto.currency.strip().upper(),
            timezone=dto.timezone.strip(),
            continent=dto.continent,
            description=dto.description.strip(),
        )

    def update_country(
        self,
        country: Country,
        dto: CountryUpdateDTO,
    ) -> Country:

        name = dto.name.strip()
        iso2 = dto.iso2.upper().strip()
        iso3 = dto.iso3.upper().strip()

        duplicate = Country.objects.exclude(
            pk=country.pk,
        )

        if duplicate.filter(name=name).exists():
            raise ValueError(
                "A country with this name already exists."
            )

        if duplicate.filter(iso2=iso2).exists():
            raise ValueError(
                "ISO2 code already exists."
            )

        if duplicate.filter(iso3=iso3).exists():
            raise ValueError(
                "ISO3 code already exists."
            )

        return self.repository.update(
            country,
            name=name,
            official_name=dto.official_name.strip(),
            iso2=iso2,
            iso3=iso3,
            phone_code=dto.phone_code.strip(),
            currency=dto.currency.strip().upper(),
            timezone=dto.timezone.strip(),
            continent=dto.continent,
            description=dto.description.strip(),
            is_active=dto.is_active,
        )

    def activate(
        self,
        country: Country,
    ) -> Country:

        return self.repository.update(
            country,
            is_active=True,
        )

    def deactivate(
        self,
        country: Country,
    ) -> Country:

        return self.repository.update(
            country,
            is_active=False,
        )

    def delete(
        self,
        country: Country,
    ) -> None:

        self.repository.delete(country)