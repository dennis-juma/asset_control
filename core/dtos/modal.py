from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ModalButtonDTO:
    label: str

    style: str = "primary"

    type: str = "button"

    url: str | None = None

    icon: str | None = None

    dismiss: bool = False


@dataclass(slots=True, frozen=True)
class ModalDTO:
    """
    Bootstrap modal DTO.
    """

    id: str

    title: str

    body: str | None = None

    size: str = ""

    scrollable: bool = False

    centered: bool = True

    static_backdrop: bool = False

    buttons: list[ModalButtonDTO] = field(default_factory=list)