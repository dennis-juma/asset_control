from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin
from core.imports.enums import ImportType
from core.imports.service import ImportService
from core.services.country_context import CountryContextService
from core.dtos.export import ExportRequestDTO
from core.exports.enums import ExportType
from core.exports.service import ExportService

from assets.dtos import (
    AssetAssignmentCreateDTO,
    AssetAssignmentUpdateDTO,
    AssetReturnDTO,
)
from assets.forms import (
    AssetAssignmentCreateForm,
    AssetAssignmentUpdateForm,
    AssetReturnForm,
)
from assets.imports import AssetAssignmentImportService
from assets.page_services import AssetAssignmentPageService
from assets.repositories import AssetAssignmentRepository
from assets.services import AssetAssignmentService


class AssetAssignmentListView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):

        page = AssetAssignmentPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
            country_context=CountryContextService.resolve_request(request),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetAssignmentExportView(PermissionRequiredMixin, TemplateView):
    permission_required = Permissions.ASSET_EXPORT

    def get(self, request, *args, **kwargs):
        export_type = request.GET.get("format", "xlsx")

        if export_type not in ("csv", "xlsx"):
            messages.error(
                request,
                "Unsupported export format.",
            )
            return redirect("assets:asset-assignment-list")

        query = request.GET.get("q", "").strip()
        queryset = AssetAssignmentRepository().export_queryset(
            query=query,
            country_context=CountryContextService.resolve_request(request),
        )

        from core.ui.datagrid import DataGridBuilder

        grid = DataGridBuilder(title="Asset Assignments")
        grid.column(field="asset_tag", label="Asset Tag")
        grid.column(field="serial_number", label="Serial Number")
        grid.column(field="assigned_to", label="Assigned To")
        grid.column(field="assignment_type", label="Assignment Type")
        grid.column(field="assigned_date", label="Assigned Date")
        grid.column(field="expected_return_date", label="Expected Return")
        grid.column(field="status", label="Status")
        grid.column(field="remarks", label="Remarks")

        for assignment in queryset:
            grid.row(
                assignment.pk,
                asset_tag=assignment.asset.asset_tag if assignment.asset else "",
                serial_number=assignment.asset.serial_number if assignment.asset else "",
                assigned_to=assignment.assigned_to_name,
                assignment_type=assignment.get_assignment_type_display() if hasattr(assignment, "get_assignment_type_display") else assignment.assignment_type,
                assigned_date=assignment.assigned_date or "",
                expected_return_date=assignment.expected_return_date or "",
                status=assignment.get_status_display(),
                remarks=assignment.remarks or "",
            )

        export_request = ExportRequestDTO(
            filename="asset_assignments",
            title="Asset Assignments",
            export_type=ExportType(export_type),
        )

        return ExportService.export(
            grid.build(),
            export_request,
        )


class AssetAssignmentImportView(View):
    template_name = "assets/assignment_import.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        action = request.POST.get("action", "preview")

        if action == "confirm":
            rows = request.session.get("asset_assignment_import_rows")
            if not rows:
                messages.error(
                    request,
                    "Import session has expired. Please upload the file again.",
                )
                return redirect("assets:asset-assignment-import")

            try:
                assignments = AssetAssignmentImportService().import_rows(rows)
            except Exception as exc:
                messages.error(
                    request,
                    f"Import failed: {exc}",
                )
                return redirect("assets:asset-assignment-import")

            request.session.pop("asset_assignment_import_rows", None)
            messages.success(
                request,
                f"{len(assignments)} assignment(s) imported successfully.",
            )
            return redirect("assets:asset-assignment-list")

        uploaded_file = request.FILES.get("file")
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
            rows = ImportService.import_file(uploaded_file, import_type)
            result = AssetAssignmentImportService().preview(rows)
        except Exception as exc:
            messages.error(
                request,
                str(exc),
            )
            return render(
                request,
                self.template_name,
            )

        request.session["asset_assignment_import_rows"] = rows
        return render(
            request,
            self.template_name,
            {
                "result": result,
                "filename": uploaded_file.name,
            },
        )


class AssetAssignmentCreateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_CREATE
    template_name = "crud/form.html"

    def get(self, request):

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().create_page(),
            }
        )

    def post(self, request):

        form = AssetAssignmentCreateForm(request.POST)

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().create_page(
                        form,
                    ),
                }
            )

        dto = AssetAssignmentCreateDTO(
        
            country=form.cleaned_data["country"],
            asset=form.cleaned_data["asset"],
            assignment_type=form.cleaned_data["assignment_type"],
            employee=form.cleaned_data["employee"],
            site=form.cleaned_data["site"],
            assigned_date=form.cleaned_data["assigned_date"],
            expected_return_date=form.cleaned_data["expected_return_date"],
            remarks=form.cleaned_data["remarks"],
        )

        AssetAssignmentService().create(dto)

        messages.success(
            request,
            "Asset assigned successfully.",
        )

        return redirect(
            "assets:asset-assignment-list",
        )


class AssetAssignmentDetailView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().detail_page(
                    assignment,
                ),
            }
        )


class AssetAssignmentUpdateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().update_page(
                    assignment,
                ),
            }
        )

    def post(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        form = AssetAssignmentUpdateForm(
            request.POST,
            instance=assignment,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().update_page(
                        assignment,
                        form,
                    ),
                }
            )

        dto = AssetAssignmentUpdateDTO(
            assignment_type=form.cleaned_data["assignment_type"],
            employee=form.cleaned_data["employee"],
            site=form.cleaned_data["site"],
            assigned_date=form.cleaned_data["assigned_date"],
            expected_return_date=form.cleaned_data["expected_return_date"],
            remarks=form.cleaned_data["remarks"],
            is_active=form.cleaned_data["is_active"],
        )

        AssetAssignmentService().update(
            assignment,
            dto,
        )

        messages.success(
            request,
            "Assignment updated successfully.",
        )

        return redirect(
            "assets:asset-assignment-list",
        )


class AssetReturnView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().return_page(
                    assignment,
                ),
            }
        )

    def post(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        form = AssetReturnForm(request.POST)

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().return_page(
                        assignment,
                        form,
                    ),
                }
            )

        dto = AssetReturnDTO(
            returned_date=form.cleaned_data["returned_date"],
            remarks=form.cleaned_data["remarks"],
        )

        AssetAssignmentService().return_asset(
            assignment,
            dto,
        )

        messages.success(
            request,
            "Asset returned successfully.",
        )

        return redirect(
            "assets:asset-assignment-detail",
            pk=assignment.pk,
        )
