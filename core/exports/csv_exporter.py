import csv

from django.http import HttpResponse

from .base import BaseExporter


class CSVExporter(BaseExporter):

    def export(self, grid, request):

        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{request.filename}.csv"'
        )

        writer = csv.writer(response)

        # Header
        writer.writerow(
            [
                column.label
                for column in grid.columns
                if column.visible
            ]
        )

        # Rows
        for row in grid.rows:

            writer.writerow(
                [
                    row.cells[column.field].display
                    for column in grid.columns
                    if column.visible
                ]
            )

        return response