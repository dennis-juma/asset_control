from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from assets.choices import AttachmentType

if TYPE_CHECKING:
    from assets.models import Asset


@dataclass
class AssetAttachmentCreateDTO:

    asset: Asset

    attachment_type: AttachmentType

    file: object

    description: str = ""


@dataclass
class AssetAttachmentUpdateDTO:

    attachment_type: AttachmentType

    description: str = ""