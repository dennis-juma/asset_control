from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class FilterOption:
    value: str
    label: str


@dataclass(slots=True, frozen=True)
class FilterField:
    name: str
    label: str
    type: str

    value: str | None = None

    placeholder: str | None = None

    options: list[FilterOption] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class FilterBar:
    fields: list[FilterField]