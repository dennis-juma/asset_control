from django import forms

from assets.choices import AttachmentType
from assets.models import AssetAttachment


class AssetAttachmentCreateForm(forms.ModelForm):
    """
    Form used to upload an attachment to an asset.
    """

    class Meta:
        model = AssetAttachment

        fields = [
            "attachment_type",
            "file",
            "description",
        ]

        widgets = {
            "attachment_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Attachment description",
                }
            ),
        }

    def __init__(
        self,
        *args,
        asset=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.asset = asset

    def clean_attachment_type(self):
        attachment_type = self.cleaned_data.get(
            "attachment_type"
        )

        if not attachment_type:
            return attachment_type

        if self.asset is None:
            raise forms.ValidationError(
                "Asset is required."
            )

        if AssetAttachment.objects.filter(
            asset=self.asset,
            attachment_type=attachment_type,
        ).exists():

            raise forms.ValidationError(
                "This attachment type already exists for this asset."
            )

        return attachment_type


class AssetAttachmentUpdateForm(forms.ModelForm):
    """
    Form used to update attachment information.

    The uploaded file itself is not replaced here.
    """

    class Meta:
        model = AssetAttachment

        fields = [
            "attachment_type",
            "description",
        ]

        widgets = {
            "attachment_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Attachment description",
                }
            ),
        }

    def __init__(
        self,
        *args,
        instance=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            instance=instance,
            **kwargs,
        )

        self.instance = instance

    def clean_attachment_type(self):
        attachment_type = self.cleaned_data.get(
            "attachment_type"
        )

        if not attachment_type:
            return attachment_type

        if self.instance is None:
            return attachment_type

        duplicate = AssetAttachment.objects.filter(
            asset=self.instance.asset,
            attachment_type=attachment_type,
        ).exclude(
            pk=self.instance.pk,
        ).exists()

        if duplicate:
            raise forms.ValidationError(
                "This attachment type already exists for this asset."
            )

        return attachment_type