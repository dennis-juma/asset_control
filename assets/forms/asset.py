from django import forms

from assets.models import Asset


class AssetCreateForm(forms.ModelForm):

    serial_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": "Enter manufacturer serial number",
            }
        ),
    )

    class Meta:
        model = Asset

        fields = [
            "country",
            "asset_model",
            "serial_number",
            "purchase_date",
            "received_date",
            "purchase_cost",
            "invoice_number",
            "condition",
            "remarks",
        ]

        widgets = {
            "purchase_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "received_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={"rows": 3},
            ),
        }


class AssetUpdateForm(forms.ModelForm):

    serial_number = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "placeholder": "Enter manufacturer serial number",
            }
        ),
    )

    class Meta:
        model = Asset

        fields = [
            "country",
            "asset_model",
            "serial_number",
            "purchase_date",
            "received_date",
            "purchase_cost",
            "invoice_number",
            "condition",
            "remarks",
            "is_active",
        ]

        widgets = {
            "purchase_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "received_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={"rows": 3},
            ),
        }