from django import forms

from assets.models import AssetModel


class AssetModelCreateForm(forms.ModelForm):

    class Meta:
        model = AssetModel

        fields = [
            "country",
            "category",
            "brand",
            "name",
            "manufacturer_part_number",
            "technical_specifications",
            "description",
        ]


class AssetModelUpdateForm(forms.ModelForm):

    class Meta:
        model = AssetModel

        fields = [
            "country",
            "category",
            "brand",
            "name",
            "manufacturer_part_number",
            "technical_specifications",
            "description",
            "is_active",
        ]