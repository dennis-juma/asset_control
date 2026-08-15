from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook

from .base import BaseExporter


class ExcelExporter(BaseExporter):

    def export(self, grid, request):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = request.title

        visible_columns = [
            column
            for column in grid.columns
            if column.visible
        ]

        # Header
        if request.include_header:
            sheet.append(
                [
                    column.label
                    for column in visible_columns
                ]
            )

        # Data rows
        for row in grid.rows:
            sheet.append(
                [
                    row.cells[column.field].display
                    for column in visible_columns
                ]
            )

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

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