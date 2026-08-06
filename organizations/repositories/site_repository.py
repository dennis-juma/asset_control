from typing import Optional

from django.core.paginator import Paginator
from django.db.models import Q

from organizations.models import Site


class SiteRepository:
    """
    Repository responsible for all Site database operations.
    """

    @staticmethod
    def create(**data) -> Site:
        return Site.objects.create(**data)



    @staticmethod
    def update(site: Site, **data) -> Site:

        for field, value in data.items():
            setattr(site, field, value)

        site.save()

        return site

    @staticmethod
    def delete(site: Site) -> None:
        site.soft_delete()


    @staticmethod
    def get(pk) -> Optional[Site]:
        return Site.objects.filter(pk=pk).first()


    @staticmethod
    def get_by_code(code: str) -> Optional[Site]:
        return Site.objects.filter(code=code).first()


    @staticmethod
    def exists(**filters) -> bool:
        return Site.objects.filter(**filters).exists()


    @staticmethod
    def active():
        return Site.objects.filter(
            is_active=True,
        ).order_by("name")




    @staticmethod
    def list(
        query="",
        page=1,
        per_page=10,
    ):
        queryset = Site.objects.select_related(
            "company",
            "country",
        ).order_by("name")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(code__icontains=query)
                | Q(city__icontains=query)
                | Q(company__name__icontains=query)
                | Q(country__name__icontains=query)
            )

        paginator = Paginator(queryset, per_page)

        return paginator.get_page(page)