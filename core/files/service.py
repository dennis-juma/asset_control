import mimetypes

from core.dtos.file import FileDTO

from .storage import FileStorageService
from .validators import FileValidator
from .enums import FileType


class FileService:

    @classmethod
    def upload(
        cls,
        uploaded_file,
        folder,
    ):

        FileValidator.validate(uploaded_file)

        path = FileStorageService.save(
            uploaded_file,
            folder,
        )

        mime = uploaded_file.content_type

        if mime.startswith("image/"):
            file_type = FileType.IMAGE

        elif mime == "application/pdf":
            file_type = FileType.PDF

        elif "spreadsheet" in mime or uploaded_file.name.endswith((".xls", ".xlsx", ".csv")):
            file_type = FileType.SPREADSHEET

        else:
            file_type = FileType.DOCUMENT

        return FileDTO(
            id=None,
            name=uploaded_file.name,
            original_name=uploaded_file.name,
            file_type=file_type,
            content_type=mime,
            size=uploaded_file.size,
            path=path,
            url=FileStorageService.url(path),
        )