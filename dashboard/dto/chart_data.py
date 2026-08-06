from dataclasses import dataclass, field

from dashboard.dto.chart_dataset import ChartDataset
from dashboard.dto.chart_options import ChartOptions
from dashboard.enums import ChartType


@dataclass(slots=True, frozen=True)
class ChartData:
    """
    Immutable DTO representing a dashboard chart.
    """

    chart_id: str

    title: str

    chart_type: ChartType

    labels: list[str]

    datasets: list[ChartDataset] = field(default_factory=list)

    options: ChartOptions = field(default_factory=ChartOptions)

    height: int = 350