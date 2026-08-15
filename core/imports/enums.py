from enum import Enum


class ImportType(str, Enum):
    CSV = "csv"
    EXCEL = "xlsx"