from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ToolbarButton:

    label: str

    icon: str

    url: str = "#"

    style: str = "primary"

    permission: str | None = None

    method: str = "GET"


@dataclass(slots=True, frozen=True)
class BulkAction:

    value: str

    label: str


@dataclass(slots=True, frozen=True)
class Toolbar:

    title: str = ""

    buttons: list[ToolbarButton] = field(default_factory=list)

    bulk_actions: list[BulkAction] = field(default_factory=list)

    show_refresh: bool = True

    show_export: bool = False

    show_import: bool = False