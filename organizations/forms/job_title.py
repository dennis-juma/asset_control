from django import forms

from organizations.models import JobTitle


class JobTitleCreateForm(forms.ModelForm):

    class Meta:
        model = JobTitle

        fields = [
            "country",
            "department",
            "name",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }


class JobTitleUpdateForm(forms.ModelForm):

    class Meta:
        model = JobTitle

        fields = [
            "country",
            "department",
            "name",
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