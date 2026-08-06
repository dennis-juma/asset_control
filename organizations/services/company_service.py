from django.db.models import query

from organizations.dtos import (
    CompanyCreateDTO,
    CompanyUpdateDTO,
)
from organizations.models import Company
from organizations.repositories import CompanyRepository


class CompanyService:



    def __init__(self):
        self.repository = CompanyRepository()

    def create_company(self, dto: CompanyCreateDTO) -> Company:

        if self.repository.exists(name=dto.name):
            raise ValueError(
                "A company with this name already exists."
            )

        return self.repository.create(
            name=dto.name,
            country=dto.country,
            legal_name=dto.legal_name,
            registration_number=dto.registration_number,
            tax_number=dto.tax_number,
            phone=dto.phone,
            email=dto.email,
            website=dto.website,
            description=dto.description,
            logo=dto.logo,
        )

    def update_company(
        self,
        company: Company,
        dto: CompanyUpdateDTO,
    ) -> Company:

        data = {
            "name": dto.name,
            "country": dto.country,
            "legal_name": dto.legal_name,
            "registration_number": dto.registration_number,
            "tax_number": dto.tax_number,
            "phone": dto.phone,
            "email": dto.email,
            "website": dto.website,
            "description": dto.description,
        }

        if dto.logo is not None:
            data["logo"] = dto.logo

        return self.repository.update(company, **data)

    def activate(self, company: Company) -> Company:
        return self.repository.update(
            company,
            is_active=True,
        )

    def deactivate(self, company: Company) -> Company:
        return self.repository.update(
            company,
            is_active=False,
        )

    def set_default(self, company: Company) -> Company:

        default = self.repository.get_default()

        if default and default.pk != company.pk:
            self.repository.update(
                default,
                is_default=False,
            )

        return self.repository.update(
            company,
            is_default=True,
        )

    def delete(self, company: Company):

        self.repository.delete(company)
