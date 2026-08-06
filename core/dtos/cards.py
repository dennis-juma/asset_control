from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class CardDTO:
    """
    Base card.
    """

    title: str

    value: str

    icon: str | None = None

    colour: str = "primary"

    subtitle: str | None = None


@dataclass(slots=True, frozen=True)
class StatCardDTO(CardDTO):
    """
    Dashboard statistic card.
    """

    trend: Decimal | None = None

    trend_label: str | None = None


@dataclass(slots=True, frozen=True)
class ProgressCardDTO(CardDTO):
    """
    Progress style card.
    """

    progress: int = 0


@dataclass(slots=True, frozen=True)
class InfoCardDTO(CardDTO):
    """
    Information card.
    """

    description: str | None = None