import os
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


def validate_attachment_file(file):
    """
    Validate uploaded asset attachment.

    Rules:
    - Maximum size: 10 MB
    - Allowed extensions:
        PDF
        JPG
        JPEG
        PNG
    """

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in settings.ALLOWED_ASSET_ATTACHMENT_EXTENSIONS:
        raise ValidationError(
            "Unsupported file type. "
            "Allowed types are: PDF, JPG, JPEG and PNG."
        )

    if file.size > settings.MAX_ASSET_ATTACHMENT_SIZE:
        raise ValidationError(
            "File size cannot exceed 10 MB."
        )

    try:
        if extension == ".pdf":
            if file.read(5) != b"%PDF-":
                raise ValidationError(
                    "The uploaded file is not a valid PDF."
                )
        else:
            image = Image.open(BytesIO(file.read()))
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValidationError(
            "The uploaded file is not a valid image."
        ) from exc
    finally:
        file.seek(0)
