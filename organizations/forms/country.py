from django import forms

from organizations.models import Country


class CountryCreateForm(forms.ModelForm):
    """
    Form used when creating a country.
    """

    class Meta:

        model = Country

        fields = [

            "name",

            "official_name",

            "iso2",

            "iso3",

            "phone_code",

            "currency",

            "timezone",

            "continent",

            "description",

            "is_active",

        ]


class CountryUpdateForm(forms.ModelForm):
    """
    Form used when updating a country.
    """

    class Meta:

        model = Country

        fields = [

            "name",

            "official_name",

            "iso2",

            "iso3",

            "phone_code",

            "currency",

            "timezone",

            "continent",

            "description",

            "is_active",

        ]