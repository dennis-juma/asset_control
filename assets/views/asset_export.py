from django.http import HttpResponse
from django.views import View

from core.dtos.export import ExportRequestDTO
from core.exports.enums import ExportType
from core.exports.service import ExportService

from assets.repositories.asset_repository import AssetRepository


class AssetExportView(View):

    def get(self, request):

        export_type = request.GET.get(
            "type",
            "csv",
        )

        try:
            export_type = ExportType(export_type)
        except ValueError:
            return HttpResponse(
                "Unsupported export type.",
                status=400,
            )

        query = request.GET.get(
            "q",
            "",
        ).strip()

        repository = AssetRepository()

        queryset = repository.export_queryset(
            query=query,
            country_context=getattr(
                request,
                "country_context",
                None,
            ),
        )

        # Build export data from the same fields shown
        # in the Asset list.
        rows = []

        for asset in queryset:

            rows.append({
                "asset_tag": asset.asset_tag,
                "serial_number": asset.serial_number,
                "category": (
                    asset.asset_model.category.name
                    if asset.asset_model
                    and asset.asset_model.category
                    else ""
                ),
                "brand": (
                    asset.asset_model.brand.name
                    if asset.asset_model
                    and asset.asset_model.brand
                    else ""
                ),
                "model": (
                    asset.asset_model.name
                    if asset.asset_model
                    else ""
                ),
                "country": (
                    asset.country.name
                    if asset.country
                    else ""
                ),
            })

        # Temporary export response construction will be
        # replaced with the DataGrid builder if your list
        # already exposes its grid definition.
        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            'attachment; filename="assets.csv"'
        )

        import csv

        writer = csv.writer(response)

        writer.writerow([
            "Asset Tag",
            "Serial Number",
            "Category",
            "Brand",
            "Model",
            "Country",
        ])

        for row in rows:
            writer.writerow([
                row["asset_tag"],
                row["serial_number"],
                row["category"],
                row["brand"],
                row["model"],
                row["country"],
            ])

        return response