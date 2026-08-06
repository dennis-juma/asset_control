from typing import Optional

from django.core.paginator import Paginator
from django.db.models import Q

from organizations.models import Country


class CountryRepository:
    """
    Repository responsible for all Country database operations.
    """

    @staticmethod
    def create(**data) -> Country:
        return Country.objects.create(**data)

    @staticmethod
    def update(country: Country, **data) -> Country:

        for field, value in data.items():
            setattr(country, field, value)

        country.save()

        return country

    @staticmethod
    def delete(country: Country) -> None:
        country.soft_delete()

    @staticmethod
    def get(pk) -> Optional[Country]:
        return Country.objects.filter(pk=pk).first()

    @staticmethod
    def get_by_code(code: str) -> Optional[Country]:
        return Country.objects.filter(code=code).first()

    @staticmethod
    def exists(**filters) -> bool:
        return Country.objects.filter(**filters).exists()

    @staticmethod
    def active():
        return Country.objects.filter(
            is_active=True
        ).order_by("name")

    @staticmethod
    def list(
        query: str = "",
        page: int = 1,
        per_page: int = 10,
    ):

        qs = Country.objects.order_by("name")

        if query:

            qs = qs.filter(

                Q(name__icontains=query) |

                Q(code__icontains=query) |

                Q(iso2__icontains=query) |

                Q(iso3__icontains=query) |

                Q(currency__icontains=query)

            )

        paginator = Paginator(
            qs,
            per_page,
        )

        return paginator.get_page(page)