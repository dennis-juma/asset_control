from django.core.paginator import Paginator

from assets.models import Asset


class AssetRepository:

    def list(
        self,
        query="",
        page=1,
        per_page=20,
        country_context=None,
    ):
        queryset = (
            Asset.objects
            .select_related(
                "country",
                "asset_model",
                "asset_model__brand",
                "asset_model__category",
            )
            .order_by("asset_tag")
        )

        if country_context and country_context.country:
            queryset = queryset.filter(
                country=country_context.country,
            )

        if query:
            queryset = queryset.filter(
                asset_tag__icontains=query,
            ) | queryset.filter(
                serial_number__icontains=query,
            ) | queryset.filter(
                asset_model__name__icontains=query,
            ) | queryset.filter(
                asset_model__brand__name__icontains=query,
            )

        return Paginator(
            queryset,
            per_page,
        ).get_page(page)

    def get(
        self,
        pk,
    ):
        return (
            Asset.objects
            .select_related(
                "country",
                "asset_model",
                "asset_model__brand",
                "asset_model__category",
            )
            .get(pk=pk)
        )

    def create(
        self,
        asset: Asset,
    ):
        asset.save()
        return asset

    def update(
        self,
        asset: Asset,
    ):
        asset.save()
        return asset

    def delete(
        self,
        asset: Asset,
    ):
        asset.delete()

    def exists_serial_number(
        self,
        serial_number: str,
        exclude_pk=None,
    ) -> bool:

        queryset = Asset.objects.filter(
            serial_number=serial_number,
        )

        if exclude_pk:
            queryset = queryset.exclude(
                pk=exclude_pk,
            )

        return queryset.exists()

    def get_by_asset_tag(
        self,
        asset_tag: str,
    ):
        return Asset.objects.get(
            asset_tag=asset_tag,
        )

    def get_by_serial_number(
        self,
        serial_number: str,
    ):
        return Asset.objects.get(
            serial_number=serial_number,
        )
