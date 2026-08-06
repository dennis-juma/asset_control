from organizations.dtos import CompanyDTO
from organizations.models import Company


class CompanyMapper:

    @staticmethod
    def to_dto(company: Company) -> CompanyDTO:
        return CompanyDTO(
            id=company.id,
            code=company.code,
            name=company.name,
            country_id=company.country_id,
            country_name=company.country.name,
            legal_name=company.legal_name,
            registration_number=company.registration_number,
            tax_number=company.tax_number,
            phone=company.phone,
            email=company.email,
            website=company.website,
            logo=company.logo.url if company.logo else None,
            description=company.description,
            is_active=company.is_active,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
