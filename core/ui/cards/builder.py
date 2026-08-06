from core.dtos.cards import (
    InfoCardDTO,
    ProgressCardDTO,
    StatCardDTO,
)


class CardBuilder:

    def stat(
        self,
        title,
        value,
        icon=None,
        colour="primary",
        trend=None,
        trend_label=None,
    ):

        return StatCardDTO(
            title=title,
            value=value,
            icon=icon,
            colour=colour,
            trend=trend,
            trend_label=trend_label,
        )

    def info(
        self,
        title,
        value,
        description=None,
        icon=None,
        colour="primary",
    ):

        return InfoCardDTO(
            title=title,
            value=value,
            icon=icon,
            colour=colour,
            description=description,
        )

    def progress(
        self,
        title,
        value,
        progress,
        icon=None,
        colour="primary",
    ):

        return ProgressCardDTO(
            title=title,
            value=value,
            progress=progress,
            icon=icon,
            colour=colour,
        )