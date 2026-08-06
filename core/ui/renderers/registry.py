from .badge import BadgeRenderer
from .boolean import BooleanRenderer
from .currency import CurrencyRenderer
from .date import DateRenderer
from .text import TextRenderer


class RendererRegistry:

    def __init__(self):

        self._renderers = {
            "text": TextRenderer(),
            "date": DateRenderer(),
            "currency": CurrencyRenderer(),
            "boolean": BooleanRenderer(),
        }

    def register(self, name, renderer):

        self._renderers[name] = renderer

    def get(self, name):

        return self._renderers[name]


registry = RendererRegistry()