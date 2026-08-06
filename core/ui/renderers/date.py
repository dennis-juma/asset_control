from datetime import date, datetime

from core.dtos import GridCell

from .base import CellRenderer


class DateRenderer(CellRenderer):

    def __init__(self, fmt="%d %b %Y"):

        self.fmt = fmt

    def render(self, value):

        if value is None:

            display = ""

        elif isinstance(value, (date, datetime)):

            display = value.strftime(self.fmt)

        else:

            display = str(value)

        return GridCell(
            value=value,
            display=display,
        )