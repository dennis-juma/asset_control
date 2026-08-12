from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AssetDetailContentDTO:
    """
    Content used by the Asset Detail page.

    Contains the existing asset form plus
    the asset attachment collection.
    """

    template: str = "components/asset/detail.html"

    asset: object = None

    form: object = None

    attachments: object = None