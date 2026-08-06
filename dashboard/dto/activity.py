from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class ActivityDTO:
    """
    Represents a single activity displayed in the dashboard timeline.
    """

    title: str
    description: str
    icon: str
    color: str
    timestamp: datetime
    url: str | None = None