from dataclasses import dataclass
from django.core.paginator import Page

from assets.dtos.asset_row import AssetRowDTO
from assets.dtos.asset_statistics import AssetStatisticsDTO


@dataclass(frozen=True, slots=True)
class AssetListDTO:
    assets: list[AssetRowDTO]
    page: Page
    statistics: AssetStatisticsDTO
    search: str = ""
    ordering: str = "-created_at"