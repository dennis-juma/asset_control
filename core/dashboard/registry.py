class DashboardRegistry:

    _widgets = {}

    @classmethod
    def register(
        cls,
        key,
        widget,
    ):

        cls._widgets[key] = widget

    @classmethod
    def get(
        cls,
        key,
    ):

        return cls._widgets[key]