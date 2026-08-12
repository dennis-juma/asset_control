from django import forms

from organizations.models import (
    Country,
    Site,
)


class SiteCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["country"].queryset = Country.objects.filter(
        is_active=True,
    )
        for field in self.fields.values():

            field.widget.attrs.update(

        {

            "class": "form-control",

        }

    )
        self.fields["country"].widget.attrs["class"] = "form-select"

        self.fields["site_type"].widget.attrs["class"] = "form-select"

    class Meta:

        model = Site

        fields = [

            "country",

            "name",

            "site_type",

            "email",

            "phone",

            "address",

            "city",

            "postal_code",

            "latitude",

            "longitude",


        ]

class SiteUpdateForm(SiteCreateForm):

    class Meta(SiteCreateForm.Meta):

        fields = SiteCreateForm.Meta.fields + [

            "is_active",

        ]
