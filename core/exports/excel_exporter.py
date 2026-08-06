from io import BytesIO

from openpyxl import Workbook
from django.http import HttpResponse

from .base import BaseExporter


class ExcelExporter(BaseExporter):

    def export(self, grid, request):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = request.title

        sheet.append(
            [
                c.label
                for c in grid.columns
                if c.visible
            ]
        )

        for row in grid.rows:

            sheet.append(
                [
                    cell.display_value
                    for cell in row.cells
                ]
            )

        output = BytesIO()

        workbook.save(output)

        response = HttpResponse(
            output.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{request.filename}.xlsx"'
        )

        return response