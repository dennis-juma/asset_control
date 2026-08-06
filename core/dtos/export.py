from dataclasses import dataclass

from core.exports.enums import ExportType


@dataclass(slots=True, frozen=True)
class ExportRequestDTO:

    filename: str

    export_type: ExportType

    title: str

    include_header: bool = True

    include_timestamp: bool = True

    include_filters: bool = False