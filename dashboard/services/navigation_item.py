from dataclasses import dataclass, field


@dataclass(slots=True)
class NavigationItem:
    title: str
    icon: str | None = None
    url: str | None = None

    children: list["NavigationItem"] = field(default_factory=list)

    permission: str | None = None

    active: bool = False

    expanded: bool = False

    badge: int | None = None