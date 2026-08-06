from dataclasses import dataclass
from enum import Enum


class ActionMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class ActionTarget(str, Enum):
    SELF = "_self"
    BLANK = "_blank"
    MODAL = "modal"


@dataclass(slots=True, frozen=True)
class ActionDTO:

    label: str

    icon: str

    url: str

    method: ActionMethod = ActionMethod.GET

    permission: str | None = None

    target: ActionTarget = ActionTarget.SELF

    css_class: str = "dropdown-item"

    confirmation: str | None = None

    danger: bool = False

    visible: bool = True