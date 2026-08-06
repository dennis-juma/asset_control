from decimal import Decimal

from core.dtos import GridCell

from .base import CellRenderer


class CurrencyRenderer(CellRenderer):

    def __init__(self, symbol="£"):

        self.symbol = symbol

    def render(self, value):

        if value is None:

            display = ""

        else:

            amount = Decimal(value)

            display = f"{self.symbol}{amount:,.2f}"

        return GridCell(
            value=value,
            display=display,
        )