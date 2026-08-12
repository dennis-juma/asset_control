from django import forms

from assets.choices import AssignmentType

from assets.models import AssetAssignment


class AssetAssignmentCreateForm(forms.ModelForm):

    class Meta:
        model = AssetAssignment

        fields = [
            "country",
            "asset",
            "assignment_type",
            "employee",
            "site",
            "assigned_date",
            "expected_return_date",
            "remarks",
        ]

        widgets = {
            "assigned_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "expected_return_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={
                    "rows": 3,
                },
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["employee"].required = False
        self.fields["site"].required = False
        self.fields["expected_return_date"].required = False




class AssetAssignmentUpdateForm(forms.ModelForm):

    class Meta:
        model = AssetAssignment

        fields = [
            "assignment_type",
            "employee",
            "site",
            "assigned_date",
            "expected_return_date",
            "remarks",
            "is_active",
        ]

        widgets = {
            "assigned_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "expected_return_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={
                    "rows": 3,
                },
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["employee"].required = False
        self.fields["site"].required = False
        self.fields["expected_return_date"].required = False




class AssetReturnForm(forms.Form):

    returned_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            },
        ),
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
            },
        ),
    )