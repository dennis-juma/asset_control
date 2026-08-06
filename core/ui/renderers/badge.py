from core.dtos import GridCell

from .base import CellRenderer


class BadgeRenderer(CellRenderer):

    def __init__(self, mapping: dict[str, str]):

        self.mapping = mapping

    def render(self, value):

        css = self.mapping.get(str(value), "secondary")

        return GridCell(
            value=value,
            display=str(value),
            renderer="badge",
            css_class=f"badge bg-{css}",
        )