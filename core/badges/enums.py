from enum import Enum


class BadgeColor(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    LIGHT = "light"
    DARK = "dark"


class BadgeSize(str, Enum):
    SM = "sm"
    MD = "md"
    LG = "lg"