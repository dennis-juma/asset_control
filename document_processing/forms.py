from django import forms
from django.core.exceptions import ValidationError

from document_processing.models import ExtractedEquipmentRecord


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(item, initial) for item in data]
        return [super().clean(data, initial)]


class UploadDocumentsForm(forms.Form):
    name = forms.CharField(max_length=200, required=False, label="Batch description")
    country = forms.ModelChoiceField(queryset=None, required=False)
    site = forms.ModelChoiceField(queryset=None, required=False)
    files = MultipleFileField(widget=MultipleFileInput(attrs={"multiple": True, "accept": "application/pdf,.pdf"}))

    def clean_files(self):
        return self.files.getlist("files")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        from organizations.models import Country, Site
        if user and not user.is_superuser and user.user_type != "SUPER_ADMIN":
            from core.services.country_context import CountryContextService
            countries = CountryContextService.get_available_countries(user)
        else:
            countries = Country.objects.filter(is_active=True)
        self.fields["country"].queryset = countries
        if user and not user.is_superuser and user.user_type != "SUPER_ADMIN":
            self.fields["country"].required = True
        self.fields["site"].queryset = Site.objects.filter(country__in=countries, is_active=True)

    def clean(self):
        cleaned = super().clean()
        files = cleaned.get("files") or []
        if not files:
            self.add_error("files", "Select at least one PDF.")
        for file in files:
            if not file.name.lower().endswith(".pdf"):
                self.add_error("files", f"{file.name}: only PDF files are supported.")
            if file.size > 20 * 1024 * 1024:
                self.add_error("files", f"{file.name}: PDF files must be 20 MB or smaller.")
            if getattr(file, "content_type", "") not in {"application/pdf", "application/x-pdf", "application/octet-stream"}:
                self.add_error("files", f"{file.name}: the uploaded content type must be PDF.")
            if file.read(5) != b"%PDF-":
                self.add_error("files", f"{file.name}: this file is not a valid PDF.")
            file.seek(0)
        site = cleaned.get("site")
        country = cleaned.get("country")
        if site and country and site.country_id != country.pk:
            self.add_error("site", "Choose a site in the selected country.")
        elif site and not country:
            cleaned["country"] = site.country
        return cleaned


class ExtractedEquipmentRecordForm(forms.ModelForm):
    class Meta:
        model = ExtractedEquipmentRecord
        fields = ["employee_name", "equipment_type", "make", "model", "serial_number", "date_received", "issued_by", "comments", "review_comments", "flagged_for_review"]
        widgets = {"date_received": forms.DateInput(format="%d/%m/%Y", attrs={"placeholder": "DD/MM/YYYY"}), "comments": forms.Textarea(attrs={"rows": 2}), "review_comments": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_received"].input_formats = ["%d/%m/%Y", "%Y-%m-%d"]
        self.fields["equipment_type"].widget = forms.Select(choices=[("", "---------"), ("Mobile Phone", "Mobile Phone"), ("Laptop/PC", "Laptop/PC"), ("Other Device / Merchandise", "Other Device / Merchandise")])

