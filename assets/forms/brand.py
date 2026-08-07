from django import forms

from assets.models import Brand


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand

        fields = [
            "company",
            "name",
            "description",
        ]


class BrandUpdateForm(forms.ModelForm):
    class Meta:
        model = Brand

        fields = [
            "company",
            "name",
            "description",
            "is_active",
        ]