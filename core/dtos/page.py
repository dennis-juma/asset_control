from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True, init=False)
class BreadcrumbDTO:
    label: str
    url: str | None = None

    def __init__(
        self,
        label: str | None = None,
        url: str | None = None,
        *,
        title: str | None = None,
        active: bool | None = None,
    ):
        """Create a breadcrumb while supporting the former ``title`` API."""
        del active
        resolved_label = label if label is not None else title
        if resolved_label is None:
            raise TypeError("BreadcrumbDTO requires either 'label' or 'title'.")

        object.__setattr__(self, "label", resolved_label)
        object.__setattr__(self, "url", url)


@dataclass(slots=True, frozen=True)
class PageDTO:
    """
    Generic application page.
    """

    title: str

    subtitle: str | None = None

    breadcrumb: list[BreadcrumbDTO] = field(default_factory=list)

    toolbar: Any = None

    statistics: list[Any] = field(default_factory=list)

    filters: Any = None

    content: Any = None

    sidebar: Any = None
