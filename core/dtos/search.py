from dataclasses import dataclass, field

from core.search.enums import SearchResultType


@dataclass(slots=True, frozen=True)
class SearchResultDTO:

    result_type: SearchResultType

    title: str

    subtitle: str

    url: str

    icon: str

    score: float = 0

    metadata: dict = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SearchResponseDTO:

    query: str

    results: list[SearchResultDTO]