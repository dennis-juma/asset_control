from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentMetadata:

    slug: str

    title: str

    category: str

    icon: str

    module: str