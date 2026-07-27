from django.db import models


class AttachmentType(models.TextChoices):
    INVOICE = "INVOICE", "Invoice"
    DELIVERY_NOTE = "DELIVERY_NOTE", "Delivery Note"