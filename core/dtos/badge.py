from dataclasses import dataclass

from core.badges.enums import (
    BadgeColor,
    BadgeSize,
)


@dataclass(slots=True, frozen=True)
class BadgeDTO:

    text: str

    color: BadgeColor

    icon: str | None = None

    tooltip: str | None = None

    pill: bool = True

    size: BadgeSize = BadgeSize.MD