from core.dtos.theme import ThemeDTO

from core.theme.enums import ThemeMode


class ThemeService:

    @staticmethod
    def current():

        return ThemeDTO(
            name="Default",
            mode=ThemeMode.LIGHT,
            primary="primary",
            secondary="secondary",
            success="success",
            warning="warning",
            danger="danger",
            info="info",
            font_family="Inter",
        )