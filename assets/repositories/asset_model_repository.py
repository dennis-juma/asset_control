from django.core.paginator import Paginator
from django.db.models import Q

from assets.models import AssetModel


class AssetModelRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=10,
    ):
        queryset = (
            AssetModel.objects
            .select_related(
                "company",
                "category",
                "brand",
            )
            .order_by(
                "brand__name",
                "name",
            )
        )

        if query:
            queryset = queryset.filter(
                Q(code__icontains=query)
                | Q(model_name__icontains=query)
                | Q(manufacturer_part_number__icontains=query)
                | Q(category__name__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(company__name__icontains=query)
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
            AssetModel.objects
            .select_related(
                "company",
                "category",
                "brand",
            )
            .get(
                pk=pk,
            )
        )

    def create(
        self,
        asset_model,
    ):
        asset_model.save()

        return asset_model

    def update(
        self,
        asset_model,
    ):
        asset_model.save()

        return asset_model

    def delete(
        self,
        asset_model,
    ):
        asset_model.delete()