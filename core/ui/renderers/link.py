from core.dtos import GridCell

from .base import CellRenderer


class LinkRenderer(CellRenderer):

    def __init__(self, url):

        self.url = url

    def render(self, value):

        return GridCell(
            value=value,
            display=str(value),
            url=self.url,
        )