from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssetStatisticsDTO:
    """
    Summary statistics displayed above the asset table.
    """

    total: int
    in_stock: int
    assigned: int
    maintenance: int
    retired: int