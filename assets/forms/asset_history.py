from django import forms
import json

from assets.models import AssetHistory


class AssetHistoryDetailForm(forms.Form):

    event_date = forms.CharField(
        label="Event Date",
        required=False,
        disabled=True,
    )

    event_type = forms.CharField(
        label="Event",
        required=False,
        disabled=True,
    )

    asset = forms.CharField(
        label="Asset",
        required=False,
        disabled=True,
    )

    company = forms.CharField(
        label="Company",
        required=False,
        disabled=True,
    )

    employee = forms.CharField(
        label="Employee",
        required=False,
        disabled=True,
    )

    site = forms.CharField(
        label="Site",
        required=False,
        disabled=True,
    )

    performed_by = forms.CharField(
        label="Performed By",
        required=False,
        disabled=True,
    )

    old_status = forms.CharField(
        label="Old Status",
        required=False,
        disabled=True,
    )

    new_status = forms.CharField(
        label="New Status",
        required=False,
        disabled=True,
    )

    reference = forms.CharField(
        label="Reference",
        required=False,
        disabled=True,
    )

    notes = forms.CharField(
        label="Notes",
        required=False,
        disabled=True,
        widget=forms.Textarea(
            attrs={"rows": 3}
        ),
    )

    metadata = forms.CharField(
        label="Metadata",
        required=False,
        disabled=True,
        widget=forms.Textarea(
            attrs={"rows": 5}
        ),
    )

    def __init__(
         self,
        *args,
        history=None,
        instance=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        history = history or instance

        if history is None:
            return

        self.initial.update({
            "event_date": (
                history.event_date.strftime(
                    "%d %b %Y %H:%M"
                )
                if history.event_date
                else ""
            ),

            "event_type": (
                history.get_event_type_display()
            ),

            "asset": (
                str(history.asset)
                if history.asset
                else ""
            ),

            "company": (
                str(history.company)
                if history.company
                else ""
            ),

            "employee": (
                str(history.employee)
                if history.employee
                else ""
            ),

            "site": (
                str(history.site)
                if history.site
                else ""
            ),

            "performed_by": (
                str(history.performed_by)
                if history.performed_by
                else "System"
            ),

            "old_status": (
                history.get_old_status_display()
                if history.old_status
                else "—"
            ),

            "new_status": (
                history.get_new_status_display()
                if history.new_status
                else "—"
            ),

            "reference": history.reference or "—",

            "notes": history.notes or "—",

            "metadata": (
    json.dumps(
        history.metadata,
        indent=4,
        ensure_ascii=False,
    )
    if history.metadata
    else "—"
),
        })