from enum import Enum


class FileType(str, Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    PDF = "pdf"
    SPREADSHEET = "spreadsheet"
    ARCHIVE = "archive"
    OTHER = "other"


class StorageBackend(str, Enum):
    LOCAL = "local"
    S3 = "s3"