from dataclasses import dataclass, field
from django.forms import BaseForm
from django.forms import BoundField


@dataclass(slots=True, frozen=True)
class FormFieldDTO:
    """
    Represents a single Django form field.
    """

    name: str

    field: BoundField

    width: int = 12

    help_text: str | None = None

    css_class: str = ""


@dataclass(slots=True, frozen=True)
class FormSectionDTO:
    """
    Represents a section within a form.
    """

    title: str

    description: str | None = None

    fields: list[FormFieldDTO] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class FormActionDTO:
    """
    Submit / Cancel buttons.
    """

    label: str

    url: str = "#"

    style: str = "primary"

    submit: bool = False

    icon: str | None = None





@dataclass(slots=True, frozen=True)
class FormDTO:

    title: str

    form: BaseForm

    template: str = "components/form.html"

    id: str = "form"

    method: str = "POST"

    action: str = ""

    enctype: str = "multipart/form-data"

    readonly: bool = False

    sections: list[FormSectionDTO] = field(default_factory=list)

    actions: list[FormActionDTO] = field(default_factory=list)

    hidden_fields: dict[str, str] = field(default_factory=dict)

    actions_alignment: str = "end"

    confirm_message: str | None = None
