class AuditLog(BaseModel):

    action = models.CharField(max_length=30)

    entity_type = models.CharField(max_length=100)

    entity_id = models.UUIDField()

    entity_name = models.CharField(max_length=255)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    before = models.JSONField(
        null=True,
        blank=True,
    )

    after = models.JSONField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    occurred_at = models.DateTimeField(
        auto_now_add=True,
    )