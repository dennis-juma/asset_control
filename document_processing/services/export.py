from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from document_processing.models import ExtractedEquipmentRecord

HEADERS = ["Record ID", "Batch Number", "Employee Name", "Equipment Type", "Make", "Model", "Serial Number", "Date Received", "Issued By", "Comments", "Source PDF", "Page Number", "Review Status", "Review Comments", "Original Extracted Values"]


def export_records(queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Extracted Records"
    sheet.append(HEADERS)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="123A52")
    for record in queryset.select_related("batch", "document"):
        sheet.append([str(record.pk), record.batch.batch_number, record.employee_name, record.equipment_type, record.make, record.model, str(record.serial_number), record.date_received.strftime("%d/%m/%Y") if record.date_received else "", record.issued_by, record.comments, record.document.original_filename, record.page_number or "", record.get_review_status_display(), record.review_comments, str(record.raw_extraction_data)])
        sheet.cell(sheet.max_row, 7).number_format = "@"
    for column, width in enumerate([38, 18, 30, 24, 18, 20, 24, 18, 25, 36, 34, 12, 18, 36, 60], 1):
        sheet.column_dimensions[get_column_letter(column)].width = width
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    instructions = workbook.create_sheet("Instructions")
    instructions.append(["Asset Document Processing — Export"])
    instructions.append(["This workbook is for review and reporting only. It cannot be re-imported into AMS."])
    instructions.append(["Record ID is the permanent staging record identifier."])
    instructions.append(["Serial Number is stored as text to preserve leading zeros."])
    instructions.append(["Mandatory review fields: Employee Name, Equipment Type, and Serial Number where present on the source checklist."])
    instructions.append(["Original Extracted Values preserves the AI response values for comparison with corrections."])
    instructions.column_dimensions["A"].width = 110
    output = BytesIO()
    workbook.save(output)
    response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="asset_document_extraction.xlsx"'
    return response

