from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class QuickActionDTO:
    """
    Represents a dashboard quick action.
    """

    title: str
    icon: str
    url: str
    color: str = "primary"