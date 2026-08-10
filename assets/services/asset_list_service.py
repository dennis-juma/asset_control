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

        search = request.GET.get("search", "").strip()
        ordering = request.GET.get("sort", "-created_at")
        page = request.GET.get("page", 1)

        queryset = self.repository.get_queryset()

        queryset = self.repository.search(
            queryset,
            search,
        )

        queryset = self.repository.filter(
            queryset,
            company=request.GET.get("company"),
            category=request.GET.get("category"),
            status=request.GET.get("status"),
        )

        queryset = self.repository.order(
            queryset,
            ordering,
        )

        page_obj = self.repository.paginate(
            queryset,
            page,
            self.PAGE_SIZE,
        )

        rows = [
            self._to_row(asset)
            for asset in page_obj.object_list
        ]


        stats = self.repository.statistics()

        statistics = AssetStatisticsDTO(
            total=stats["total"],
            assigned=stats["assigned"],
            in_stock=stats["in_stock"],
            maintenance=stats["maintenance"],
            retired=stats["retired"],
        )

        return AssetListDTO(
    assets=rows,
    page=page_obj,
    statistics=statistics,
    search=search,
    ordering=ordering,
)

    def _to_row(self, asset):

        return AssetRowDTO(
            id=asset.id,
            asset_tag=asset.asset_tag,
            serial_number=asset.serial_number,
            barcode=asset.barcode,
            company=asset.company.name if asset.company else None,
            category=asset.category.name if asset.category else None,
            brand=asset.brand.name if asset.brand else None,
            model=asset.model.name if asset.model else None,
            vendor=asset.vendor.name if asset.vendor else None,
            status=asset.get_status_display(),
            condition=asset.get_condition_display(),
            purchase_date=asset.purchase_date,
            purchase_price=asset.purchase_price,
            under_warranty=asset.is_under_warranty,
        )
    
