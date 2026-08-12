from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AssetAttachmentsContentDTO:

    template: str = "components/asset/attachments.html"

    asset: object = None

    attachments: object = None