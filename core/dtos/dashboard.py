from dataclasses import dataclass, field
from typing import Any

from core.dashboard.enums import WidgetType


@dataclass(slots=True, frozen=True)
class DashboardWidgetDTO:

    id: str

    title: str

    widget_type: WidgetType

    template: str

    data: Any

    width: int = 12

    refreshable: bool = False

    refresh_interval: int | None = None

    permission: str | None = None


@dataclass(slots=True, frozen=True)
class DashboardDTO:

    title: str

    widgets: list[DashboardWidgetDTO] = field(default_factory=list)