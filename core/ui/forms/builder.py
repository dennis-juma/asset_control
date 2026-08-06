from django.urls import reverse

from core.dtos.forms import (
    FormActionDTO,
    FormDTO,
    FormFieldDTO,
    FormSectionDTO,
)


class FormBuilder:

    def __init__(
        self,
        title: str,
        form,
        action="",
        method="POST",
    ):

        self.form = FormDTO(
            title=title,
            form=form,
            action=action,
            method=method,
        )

        self._current_section = None

    def section(
        self,
        title,
        description=None,
    ):

        section = FormSectionDTO(
            title=title,
            description=description,
            fields=[],
        )

        self.form.sections.append(section)

        self._current_section = section

        return self

    def field(
        self,
        name,
        width=12,
    ):

        if self._current_section is None:
            raise ValueError(
                "Call section() before field()."
            )

        self._current_section.fields.append(
            FormFieldDTO(
                name=name,
                field=self.form.form[name],
                width=width,
            )
        )

        return self

    def submit(
        self,
        label="Save",
        icon="bi-check-circle",
    ):

        self.form.actions.append(
            FormActionDTO(
                label=label,
                submit=True,
                icon=icon,
            )
        )

        return self

    def cancel(
        self,
        url,
        label="Cancel",
    ):

        self.form.actions.append(
            FormActionDTO(
                label=label,
                url=url,
                style="secondary",
            )
        )

        return self

    def reverse(
        self,
        url_name,
        args=None,
        kwargs=None,
        label="Cancel",
    ):
        """
        Add a Cancel button using a Django URL name.

        Example:
            .reverse("organizations:country-list")

            .reverse(
                "organizations:country-detail",
                args=[country.id],
            )
        """

        return self.cancel(
            url=reverse(
                url_name,
                args=args,
                kwargs=kwargs,
            ),
            label=label,
        )

    def build(self):

        return self.form