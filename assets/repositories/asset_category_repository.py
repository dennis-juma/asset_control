from django.core.paginator import Paginator
from django.db.models import Q

from assets.models import AssetCategory


class AssetCategoryRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
        country_context=None,
    ):
        queryset = (
            AssetCategory.objects
            .select_related(
                "country",
                "parent",
            )
            .order_by(
                "sort_order",
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
                | Q(country__name__icontains=query)
                | Q(parent__name__icontains=query)
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
            AssetCategory.objects
            .select_related(
                "country",
                "parent",
            )
            .get(
                pk=pk,
            )
        )

    def create(
        self,
        category,
    ):
        category.save()

        return category

    def update(
        self,
        category,
    ):
        category.save()

        return category

    def delete(
        self,
        category,
    ):
        category.delete()
