class AuditService:

    @classmethod
    def record(
        cls,
        dto: AuditDTO,
    ):

        from core.models.audit_log import AuditLog

        AuditLog.objects.create(
            action=dto.action,
            entity_type=dto.entity_type,
            entity_id=dto.entity_id,
            entity_name=dto.entity_name,
            actor_id=dto.actor_id,
            before=dto.before,
            after=dto.after,
            metadata=dto.metadata or {},
        )
