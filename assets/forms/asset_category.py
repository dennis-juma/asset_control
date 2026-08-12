from django import forms

from assets.models import AssetCategory


class AssetCategoryCreateForm(forms.ModelForm):

    class Meta:
        model = AssetCategory

        fields = [
            "country",
            "parent",
            "name",
            "description",
            "sort_order",
        ]


class AssetCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = AssetCategory

        fields = [
            "country",
            "parent",
            "name",
            "description",
            "sort_order",
            "is_active",
        ]