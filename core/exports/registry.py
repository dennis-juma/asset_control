from .csv_exporter import CSVExporter
from .excel_exporter import ExcelExporter


class ExportRegistry:

    EXPORTERS = {
        "csv": CSVExporter(),
        "xlsx": ExcelExporter(),
    }