from pathlib import Path

from django.core.exceptions import ValidationError


class FileValidator:

    MAX_SIZE = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf",
        ".xlsx",
        ".xls",
        ".csv",
        ".docx",
    }

    @classmethod
    def validate(cls, uploaded_file):

        if uploaded_file.size > cls.MAX_SIZE:
            raise ValidationError("File exceeds maximum allowed size.")

        extension = Path(uploaded_file.name).suffix.lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise ValidationError("Unsupported file type.")