from .registry import ImportRegistry
from .exceptions import ImportFileError


class ImportService:

    @classmethod
    def import_file(
        cls,
        uploaded_file,
        import_type,
    ):

        importer = ImportRegistry.IMPORTERS.get(
            import_type.value
            if hasattr(import_type, "value")
            else import_type
        )

        if importer is None:
            raise ImportFileError(
                f"Unsupported import type: {import_type}"
            )

        return importer.read(
            uploaded_file
        )