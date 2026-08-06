from enum import Enum


class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class ButtonStyle(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    OUTLINE = "outline"


class IconSize(str, Enum):
    SM = "fs-6"
    MD = "fs-5"
    LG = "fs-4"
    XL = "fs-2"