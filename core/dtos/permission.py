from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PermissionResultDTO:

    permission: str

    allowed: bool

    reason: str | None = None