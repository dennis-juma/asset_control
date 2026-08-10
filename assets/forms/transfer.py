from django import forms

from assets.choices import AssignmentType
from employees.models import Employee
from organizations.models import Site


class AssetTransferCreateForm(forms.Form):
    """
    Form used to transfer an assigned asset.
    """

    assignment_type = forms.ChoiceField(
        label="Transfer To",
        choices=AssignmentType.choices,
        initial=AssignmentType.EMPLOYEE,
        widget=forms.RadioSelect,
    )

    employee = forms.ModelChoiceField(
        label="Employee",
        queryset=Employee.objects.filter(
            is_active=True,
        ),
        required=False,
        empty_label="Select Employee",
    )

    site = forms.ModelChoiceField(
        label="Site",
        queryset=Site.objects.filter(
            is_active=True,
        ),
        required=False,
        empty_label="Select Site",
    )

    transfer_date = forms.DateField(
        label="Transfer Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    reason = forms.CharField(
        label="Reason",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Reason for transfer",
            }
        ),
    )

    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Additional remarks",
            }
        ),
    )

    def __init__(
    self,
    *args,
    asset=None,
    previous_assignment=None,
    **kwargs,
):
        super().__init__(*args, **kwargs)

        self.asset = asset
        self.previous_assignment = previous_assignment

        if previous_assignment is not None:

            # ---------------------------------------------
            # Current employee
            # ---------------------------------------------

            if previous_assignment.employee_id:

                self.fields["employee"].queryset = (
                    Employee.objects
                    .filter(is_active=True)
                    .exclude(
                        pk=previous_assignment.employee_id
                    )
                )

            # ---------------------------------------------
            # Current site
            # ---------------------------------------------

            if previous_assignment.site_id:

                self.fields["site"].queryset = (
                    Site.objects
                    .filter(is_active=True)
                    .exclude(
                        pk=previous_assignment.site_id
                    )
                )

    def clean(self):
        cleaned_data = super().clean()

        assignment_type = cleaned_data.get("assignment_type")
        employee = cleaned_data.get("employee")
        site = cleaned_data.get("site")

        # Normalize AssignmentType
        if assignment_type == AssignmentType.EMPLOYEE.value:
            assignment_type = AssignmentType.EMPLOYEE

        elif assignment_type == AssignmentType.SITE.value:
            assignment_type = AssignmentType.SITE

        # -------------------------------------------------
        # Employee transfer
        # -------------------------------------------------

        if assignment_type == AssignmentType.EMPLOYEE:

            # Site is NEVER a target for Employee transfer
            cleaned_data["site"] = None

            if employee is None:
                self.add_error(
                    "employee",
                    "Please select an employee.",
                )

        # -------------------------------------------------
        # Site transfer
        # -------------------------------------------------

        elif assignment_type == AssignmentType.SITE:

            # Employee is NEVER a target for Site transfer
            cleaned_data["employee"] = None

            if site is None:
                self.add_error(
                    "site",
                    "Please select a site.",
                )

        else:

            self.add_error(
                "assignment_type",
                "Please select either Employee or Site.",
            )

        return cleaned_data


class AssetTransferUpdateForm(forms.Form):
    """
    Form used to update transfer information.

    Source and target are intentionally not editable because
    they are part of the historical transaction.
    """

    transfer_date = forms.DateField(
        label="Transfer Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    reason = forms.CharField(
        label="Reason",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Reason for transfer",
            }
        ),
    )

    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Additional remarks",
            }
        ),
    )

    is_active = forms.BooleanField(
        label="Active",
        required=False,
    )

    def __init__(
        self,
        *args,
        instance=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.instance = instance

        if instance is not None and not self.is_bound:

            self.fields[
                "transfer_date"
            ].initial = instance.transfer_date

            self.fields[
                "reason"
            ].initial = instance.reason

            self.fields[
                "remarks"
            ].initial = instance.remarks

            self.fields[
                "is_active"
            ].initial = instance.is_active