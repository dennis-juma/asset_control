from dataclasses import dataclass
from uuid import UUID

from core.files.enums import FileType


@dataclass(slots=True, frozen=True)
class FileDTO:

    id: UUID | None

    name: str

    original_name: str

    file_type: FileType

    content_type: str

    size: int

    path: str

    url: str

    checksum: str | None = None

    thumbnail_url: str | None = None