from dataclasses import dataclass

from .dashboard_layout import DashboardLayoutDTO


@dataclass(slots=True, frozen=True)
class DashboardPageDTO:

    title: str

    description: str | None

    layout: DashboardLayoutDTO

    refresh_interval: int | None = None
