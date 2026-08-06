class ThemeRegistry:

    THEMES = {}

    @classmethod
    def register(
        cls,
        name,
        theme,
    ):
        cls.THEMES[name] = theme

    @classmethod
    def get(
        cls,
        name,
    ):
        return cls.THEMES[name]