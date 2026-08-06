from django import forms

from organizations.models import Department


class DepartmentCreateForm(forms.ModelForm):

    class Meta:
        model = Department

        fields = [
            "company",
            "site",
            "parent",
            "name",
            "cost_center",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }


class DepartmentUpdateForm(forms.ModelForm):

    class Meta:
        model = Department

        fields = [
            "company",
            "site",
            "parent",
            "name",
            "cost_center",
            "description",
            "is_active",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }