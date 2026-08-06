from dataclasses import dataclass

from core.theme.enums import ThemeMode


@dataclass(slots=True, frozen=True)
class ThemeDTO:

    name: str

    mode: ThemeMode

    primary: str

    secondary: str

    success: str

    warning: str

    danger: str

    info: str

    font_family: str

    logo: str | None = None