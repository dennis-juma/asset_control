from dataclasses import dataclass

from dashboard.enums import StatFormatter


@dataclass(slots=True, frozen=True)
class StatCard:
    """
    Immutable DTO representing a dashboard KPI card.
    """

    title: str
    value: int | float
    icon: str
    color: str

    subtitle: str = ""

    trend: float | None = None
    trend_direction: str | None = None

    formatter: StatFormatter = StatFormatter.NUMBER