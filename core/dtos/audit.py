from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class AuditDTO:

    action: str

    entity_type: str

    entity_id: str

    entity_name: str

    actor_id: str | None

    actor_name: str | None

    occurred_at: datetime

    before: dict[str, Any] | None = None

    after: dict[str, Any] | None = None

    metadata: dict[str, Any] | None = None