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

        writer.writerow(
            [
                c.label
                for c in grid.columns
                if c.visible
            ]
        )

        for row in grid.rows:

            writer.writerow(
                [
                    cell.display_value
                    for cell in row.cells
                ]
            )

        return response