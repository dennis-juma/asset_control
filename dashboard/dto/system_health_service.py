from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HealthItemDTO:
    """
    Represents a single system health item.
    """

    title: str
    status: str
    icon: str
    color: str


@dataclass(slots=True, frozen=True)
class SystemHealthDTO:
    """
    Dashboard system health summary.
    """

    items: list[HealthItemDTO]
    last_backup: str
    version: str