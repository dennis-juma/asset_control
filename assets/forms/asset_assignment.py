from django import forms

from assets.choices import AssignmentStatus, AssignmentType, AssetStatus
from assets.models import Asset, AssetAssignment
from employees.models import Employee
from organizations.models import Site


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
            "assignment_type": forms.RadioSelect,
            "assigned_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control assignment-date-input"},
            ),
            "expected_return_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control assignment-date-input"},
            ),
            "remarks": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control assignment-remarks-field",
                },
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["asset"].queryset = (
            Asset.objects
            .filter(status=AssetStatus.AVAILABLE)
            .exclude(assignments__status=AssignmentStatus.ACTIVE)
            .select_related(
                "asset_model",
                "asset_model__category",
                "asset_model__brand",
                "country",
            )
            .order_by("asset_tag")
        )

        self.fields["employee"].queryset = (
            Employee.objects
            .filter(is_active=True)
            .select_related(
                "country",
                "site",
                "department",
                "job_title",
            )
            .order_by("employee_id")
        )

        self.fields["site"].queryset = (
            Site.objects
            .filter(is_active=True)
            .order_by("name")
        )

        self.fields["country"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search country...",
        })
        self.fields["assignment_type"].widget.attrs.pop("class", None)
        self.fields["employee"].required = False
        self.fields["site"].required = False
        self.fields["expected_return_date"].required = False

        from django.urls import reverse

        self.fields["asset"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search asset...",
        })
        self.fields["employee"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search employee...",
            "data-ajax-url": reverse("employees:employee-autocomplete"),
        })
        self.fields["site"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search site...",
        })
        self.fields["assigned_date"].widget.attrs.update({
            "class": "form-control assignment-date-input",
            "data-placeholder": "Select assigned date...",
        })
        self.fields["expected_return_date"].widget.attrs.update({
            "class": "form-control assignment-date-input",
            "data-placeholder": "Select expected return date...",
        })
        self.fields["remarks"].widget.attrs.update({
            "class": "form-control assignment-remarks-field",
            "placeholder": "Add notes or remarks for the assignment...",
        })


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
                attrs={"type": "date", "class": "form-control assignment-date-input"},
            ),
            "expected_return_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control assignment-date-input"},
            ),
            "remarks": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control assignment-remarks-field",
                },
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["employee"].queryset = (
            Employee.objects
            .filter(is_active=True)
            .select_related(
                "country",
                "site",
                "department",
                "job_title",
            )
            .order_by("employee_id")
        )

        self.fields["site"].queryset = (
            Site.objects
            .filter(is_active=True)
            .order_by("name")
        )

        self.fields["employee"].required = False
        self.fields["site"].required = False
        self.fields["expected_return_date"].required = False

        from django.urls import reverse

        self.fields["employee"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search employee...",
            "data-ajax-url": reverse("employees:employee-autocomplete"),
        })
        self.fields["site"].widget.attrs.update({
            "class": "form-select tom-select",
            "data-placeholder": "Search site...",
        })
        self.fields["assigned_date"].widget.attrs.update({
            "class": "form-control assignment-date-input",
            "data-placeholder": "Select assigned date...",
        })
        self.fields["expected_return_date"].widget.attrs.update({
            "class": "form-control assignment-date-input",
            "data-placeholder": "Select expected return date...",
        })
        self.fields["remarks"].widget.attrs.update({
            "class": "form-control assignment-remarks-field",
            "placeholder": "Add notes or remarks for the assignment...",
        })


class AssetReturnForm(forms.Form):

    returned_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control assignment-date-input",
            },
        ),
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control assignment-remarks-field",
                "placeholder": "Add return notes...",
            },
        ),
    )