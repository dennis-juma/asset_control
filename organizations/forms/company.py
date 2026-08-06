from django import forms

from organizations.models import Company


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = [
            "name",
            "country",
            "legal_name",
            "registration_number",
            "tax_number",
            "phone",
            "email",
            "website",
            "description",
            "logo",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }



class CompanyUpdateForm(CompanyCreateForm):
    pass
