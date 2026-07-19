import os

from django.core.exceptions import ValidationError


def validate_pdf(value):
    ext = os.path.splitext(value.name)[1].lower()

    if ext != ".pdf":
        raise ValidationError("Only PDF files are allowed.")


def validate_image(value):
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in [".jpg", ".jpeg", ".png"]:
        raise ValidationError(
            "Upload JPG, JPEG or PNG images."
        )


def validate_file_size(value):
    limit = 20 * 1024 * 1024

    if value.size > limit:
        raise ValidationError(
            "Maximum upload size is 20 MB."
        )