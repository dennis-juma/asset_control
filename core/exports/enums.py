from enum import Enum


class ExportType(str, Enum):
    CSV = "csv"
    EXCEL = "xlsx"
    PDF = "pdf"
    PRINT = "print"