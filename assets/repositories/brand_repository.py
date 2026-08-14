from django.core.paginator import Paginator
from django.db.models import Q

from assets.models import Brand


class BrandRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
        country_context=None,
    ):
        queryset = (
            Brand.objects
            .select_related(
                "country",
            )
            .order_by(
                "name",
            )
        )

        if country_context and country_context.country:
            queryset = queryset.filter(
                country=country_context.country,
            )

        if query:
            queryset = queryset.filter(
                Q(code__icontains=query)
                | Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(country__name__icontains=query)
            )

        paginator = Paginator(
            queryset,
            per_page,
        )

        return paginator.get_page(page)

    def get(
        self,
        pk,
    ):
        return (
            Brand.objects
            .select_related(
                "country",
            )
            .get(
                pk=pk,
            )
        )

    def create(
        self,
        brand,
    ):
        brand.save()

        return brand

    def update(
        self,
        brand,
    ):
        brand.save()

        return brand

    def delete(
        self,
        brand,
    ):
        brand.delete()
