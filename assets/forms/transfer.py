from django import forms
from django.utils import timezone

from employees.models import Employee


class AssetTransferForm(forms.Form):
    """
    Form used to transfer an asset from one employee to another.
    """

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True),
        label="Transfer To",
        empty_label="Select Employee",
    )

    assigned_date = forms.DateField(
        initial=timezone.now().date,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    expected_return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Reason for transfer...",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        assigned_date = cleaned_data.get("assigned_date")
        expected_return = cleaned_data.get("expected_return_date")

        if (
            assigned_date
            and expected_return
            and expected_return < assigned_date
        ):
            self.add_error(
                "expected_return_date",
                "Expected return date cannot be before assigned date.",
            )

        return cleaned_data