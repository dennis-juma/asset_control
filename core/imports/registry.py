from .csv.importer import CSVImporter
from .excel.importer import ExcelImporter


class ImportRegistry:

    IMPORTERS = {
        "csv": CSVImporter(),
        "xlsx": ExcelImporter(),
    }