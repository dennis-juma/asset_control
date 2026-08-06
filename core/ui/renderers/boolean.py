from core.dtos import GridCell

from .base import CellRenderer


class BooleanRenderer(CellRenderer):

    def render(self, value):

        return GridCell(
            value=value,
            display="Yes" if value else "No",
            renderer="badge",
            css_class=f"badge bg-{'success' if value else 'secondary'}",
        )