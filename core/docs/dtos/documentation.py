from dataclasses import dataclass, field

from .section import DocumentationSectionDTO


@dataclass(slots=True)
class DocumentationDTO:
    """
    Represents a documentation page.
    """

    title: str

    slug: str

    description: str

    version: str = "1.0"

    category: str = "General"

    icon: str = "book"

    sections: list[DocumentationSectionDTO] = field(
        default_factory=list
    )

    related: list[str] = field(
        default_factory=list
    )

    navigation: list[str] = field(
        default_factory=list
    )