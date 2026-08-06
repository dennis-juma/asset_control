from dataclasses import dataclass, field
from datetime import datetime

from core.ui.timeline.enums import TimelineLevel


@dataclass(slots=True, frozen=True)
class TimelineMetadataDTO:
    label: str
    value: str


@dataclass(slots=True, frozen=True)
class TimelineItemDTO:

    title: str

    description: str

    occurred_at: datetime

    icon: str

    level: TimelineLevel = TimelineLevel.PRIMARY

    actor: str | None = None

    metadata: list[TimelineMetadataDTO] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class TimelineGroupDTO:

    date: str

    items: list[TimelineItemDTO]


@dataclass(slots=True, frozen=True)
class TimelineDTO:

    groups: list[TimelineGroupDTO]