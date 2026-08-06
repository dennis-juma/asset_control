from core.dtos import GridCell

from .base import CellRenderer


class TextRenderer(CellRenderer):

    def render(self, value):

        return GridCell(
            value=value,
            display="" if value is None else str(value),
        )