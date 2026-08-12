from django import forms

from assets.models import Brand


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand

        fields = [
            "country",
            "name",
            "description",
        ]


class BrandUpdateForm(forms.ModelForm):
    class Meta:
        model = Brand

        fields = [
            "country",
            "name",
            "description",
            "is_active",
        ]