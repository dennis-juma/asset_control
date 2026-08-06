from django import forms

from assets.models import AssetCategory


class AssetCategoryCreateForm(forms.ModelForm):

    class Meta:
        model = AssetCategory

        fields = [
            "company",
            "parent",
            "name",
            "description",
            "sort_order",
        ]


class AssetCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = AssetCategory

        fields = [
            "company",
            "parent",
            "name",
            "description",
            "sort_order",
            "is_active",
        ]