from typing import Optional

from organizations.models import Company

from django.db.models import Q

from django.core.paginator import Paginator


class CompanyRepository:
    """
    Repository responsible for all Company database operations.
    """

    @staticmethod
    def create(**data) -> Company:
        return Company.objects.create(**data)

    @staticmethod
    def update(company: Company, **data) -> Company:
        for field, value in data.items():
            setattr(company, field, value)

        company.save()
        return company

    @staticmethod
    def delete(company: Company) -> None:
        company.soft_delete()

    @staticmethod
    def get(pk) -> Optional[Company]:
        return Company.objects.filter(pk=pk).first()

    @staticmethod
    def get_by_code(code: str) -> Optional[Company]:
        return Company.objects.filter(code=code).first()

    @staticmethod
    def exists(**filters) -> bool:
        return Company.objects.filter(**filters).exists()

   

    @staticmethod
    def active():
        return Company.objects.filter(
            is_active=True
        ).order_by("name")

    @staticmethod
    def list(query: str = "", page: int = 1, per_page: int = 10):

        qs = Company.objects.order_by("name")

        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(code__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )

        paginator = Paginator(qs, per_page)
        return paginator.get_page(page)
