from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class DocumentationSectionDTO:
    """
    Represents a single section within a documentation page.
    """

    title: str

    component: str

    content: Any = None

    description: str | None = None

    order: int = 0

    collapsible: bool = False

    collapsed: bool = False

    css_class: str = ""