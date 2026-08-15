from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

from core.imports.enums import ImportType
from core.imports.service import ImportService

from assets.imports import AssetImportService


class AssetImportView(View):

    template_name = "assets/import.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):

        action = request.POST.get(
            "action",
            "preview",
        )

        # =====================================================
        # CONFIRM IMPORT
        # =====================================================

        if action == "confirm":

            rows = request.session.get(
                "asset_import_rows"
            )

            if not rows:
                messages.error(
                    request,
                    "Import session has expired. Please upload the file again.",
                )

                return redirect(
                    "assets:asset-import"
                )

            try:
                assets = AssetImportService().confirm(
                    rows
                )

            except ValidationError as exc:

                messages.error(
                    request,
                    str(exc),
                )

                return redirect(
                    "assets:asset-import"
                )

            except Exception as exc:

                messages.error(
                    request,
                    f"Import failed: {exc}",
                )

                return redirect(
                    "assets:asset-import"
                )

            request.session.pop(
                "asset_import_rows",
                None,
            )

            messages.success(
                request,
                f"{len(assets)} asset(s) imported successfully.",
            )

            return redirect(
                "assets:asset-list"
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

            result = AssetImportService().preview(
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

        request.session["asset_import_rows"] = rows

        return render(
            request,
            self.template_name,
            {
                "result": result,
                "filename": uploaded_file.name,
            },
        )