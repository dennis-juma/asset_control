from django.utils import timezone

from core.audit.service import AuditService
from core.dtos.audit import AuditDTO


def record_audit(action, entity_type, instance, *, user=None, before=None, after=None, metadata=None):
    AuditService.record(AuditDTO(action=action, entity_type=entity_type, entity_id=str(instance.pk), entity_name=str(instance)[:255], actor_id=str(user.pk) if user else None, actor_name=user.get_username() if user else None, occurred_at=timezone.now(), before=before, after=after, metadata=metadata or {}))

