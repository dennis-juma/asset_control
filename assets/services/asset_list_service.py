from assets.dtos import (
    AssetListDTO,
    AssetRowDTO,
    AssetStatisticsDTO,
)
from assets.repositories import AssetRepository


class AssetListService:
    """
    Service responsible for preparing data for the Asset List page.
    """

    PAGE_SIZE = 25

    def __init__(self):
        self.repository = AssetRepository()

    def get_asset_list(self, request) -> AssetListDTO:

        search = request.GET.get(
            "search",
            "",
        ).strip()

        page = request.GET.get(
            "page",
            1,
        )

        page_obj = self.repository.list(
            query=search,
            page=page,
            per_page=self.PAGE_SIZE,
        )

        rows = [
            self._to_row(asset)
            for asset in page_obj.object_list
        ]

        statistics = self._get_statistics()

        return AssetListDTO(
            assets=rows,
            page=page_obj,
            statistics=statistics,
            search=search,
            ordering=request.GET.get(
                "sort",
                "-created_at",
            ),
        )

    def get_export_queryset(self, request):

        search = request.GET.get(
            "search",
            "",
        ).strip()

        return self.repository.export_queryset(
            query=search,
        )

    def _get_statistics(self):

        queryset = self.repository._base_queryset()

        return AssetStatisticsDTO(
            total=queryset.count(),

            assigned=queryset.filter(
                status="ASSIGNED",
            ).count(),

            in_stock=queryset.filter(
                status="AVAILABLE",
            ).count(),

            maintenance=queryset.filter(
                status="MAINTENANCE",
            ).count(),

            retired=queryset.filter(
                status="RETIRED",
            ).count(),
        )

    def _to_row(self, asset):

        return AssetRowDTO(
            id=asset.id,
            asset_tag=asset.asset_tag,
            serial_number=asset.serial_number,

            country=(
                asset.country.name
                if asset.country
                else None
            ),

            category=(
                asset.asset_model.category.name
                if asset.asset_model
                else None
            ),

            brand=(
                asset.asset_model.brand.name
                if asset.asset_model
                else None
            ),

            model=(
                asset.asset_model.name
                if asset.asset_model
                else None
            ),

            status=asset.get_status_display(),
            condition=asset.get_condition_display(),

            purchase_date=asset.purchase_date,
            received_date=asset.received_date,
            purchase_cost=asset.purchase_cost,
            invoice_number=asset.invoice_number,
        )