from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AlertDTO:
    title: str
    description: str
    icon: str
    color: str
    count: int
    url: str | None = None