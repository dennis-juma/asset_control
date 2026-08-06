from core.exports.registry import ExportRegistry


class ExportService:

    @classmethod
    def export(
        cls,
        grid,
        request,
    ):

        exporter = ExportRegistry.EXPORTERS[
            request.export_type.value
        ]

        return exporter.export(
            grid,
            request,
        )