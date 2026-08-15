class ImportError(Exception):
    """Base exception for import failures."""


class ImportFileError(ImportError):
    """Invalid or unreadable import file."""


class ImportValidationError(ImportError):
    """Import data contains validation errors."""