from dataclasses import dataclass, field

from .dashboard import DashboardWidgetDTO


@dataclass(slots=True, frozen=True)
class DashboardLayoutDTO:

    columns: int

    gap: int = 3

    widgets: list[DashboardWidgetDTO] = field(
        default_factory=list
    )
