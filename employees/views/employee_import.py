from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

from core.imports.enums import ImportType
from core.imports.service import ImportService

from employees.imports import EmployeeImportService


class EmployeeImportView(View):

    template_name = "employees/import.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):

        # =====================================================
        # CONFIRM IMPORT
        # =====================================================

        action = request.POST.get(
            "action",
            "preview",
        )

        if action == "confirm":

            rows = request.session.get(
                "employee_import_rows"
            )

            if not rows:
                messages.error(
                    request,
                    "Import session has expired. Please upload the file again.",
                )

                return redirect(
                    "employees:employee-import"
                )

            try:
                employees = EmployeeImportService().import_rows(
                    rows
                )

            except ValidationError as exc:

                messages.error(
                    request,
                    str(exc),
                )

                return redirect(
                    "employees:employee-import"
                )

            except Exception as exc:

                messages.error(
                    request,
                    f"Import failed: {exc}",
                )

                return redirect(
                    "employees:employee-import"
                )

            request.session.pop(
                "employee_import_rows",
                None,
            )

            messages.success(
                request,
                f"{len(employees)} employee(s) imported successfully.",
            )

            return redirect(
                "employees:employee-list"
            )

        # =====================================================
        # PREVIEW
        # =====================================================

        uploaded_file = request.FILES.get(
            "file"
        )

        if not uploaded_file:

            messages.error(
                request,
                "Please select a CSV or Excel file.",
            )

            return render(
                request,
                self.template_name,
            )

        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            import_type = ImportType.CSV

        elif filename.endswith(".xlsx"):
            import_type = ImportType.EXCEL

        else:

            messages.error(
                request,
                "Only CSV and XLSX files are supported.",
            )

            return render(
                request,
                self.template_name,
            )

        try:

            rows = ImportService.import_file(
                uploaded_file,
                import_type,
            )

            result = EmployeeImportService().preview(
                rows
            )

        except Exception as exc:

            messages.error(
                request,
                str(exc),
            )

            return render(
                request,
                self.template_name,
            )

        request.session[
            "employee_import_rows"
        ] = rows

        return render(
            request,
            self.template_name,
            {
                "result": result,
                "filename": uploaded_file.name,
            },
        )