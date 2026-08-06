from dataclasses import dataclass

from core.theme.enums import ButtonStyle


@dataclass(frozen=True)
class ButtonTheme:

    style: ButtonStyle

    icon: str | None = None


class ThemeButtons:

    SAVE = ButtonTheme(
        ButtonStyle.SUCCESS,
        "bi-check-circle",
    )

    DELETE = ButtonTheme(
        ButtonStyle.DANGER,
        "bi-trash",
    )

    EDIT = ButtonTheme(
        ButtonStyle.PRIMARY,
        "bi-pencil",
    )

    CANCEL = ButtonTheme(
        ButtonStyle.SECONDARY,
        "bi-x-circle",
    )