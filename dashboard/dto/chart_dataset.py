from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ChartDataset:
    """
    Immutable dataset for a dashboard chart.
    """

    label: str

    data: list[int | float]

    background_color: list[str] = field(default_factory=list)

    border_color: list[str] = field(default_factory=list)

    border_width: int = 2

    fill: bool = False

    tension: float = 0.4