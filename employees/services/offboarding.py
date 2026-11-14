from django.db import transaction
from django.utils import timezone

from assets.services.asset_notification_service import AssetNotificationService
from core.audit.service import AuditService
from core.dtos.audit import AuditDTO
from core.notifications.enums import NotificationEvent
from core.notifications.email import NotificationEmailService
from core.notifications.service import NotificationService
from employees.models import Employee


OFFBOARDING_SUBJECT = "Employee Offboarding - Asset Return Required"


@transaction.atomic
def offboard_employee_for_exit(employee_id, *, due_date):
    """Offboard one due employee once, including email and audit history."""
    employee = (
        Employee.objects.select_for_update()
        .filter(
            pk=employee_id,
            is_active=True,
            last_working_date__lte=due_date,
        )
        .first()
    )
    if employee is None:
        return False

    now = timezone.now()
    user = employee.user if employee.user_id else None
    assigned_assets = list(AssetNotificationService.employee_assets(employee))
    subject = f"{OFFBOARDING_SUBJECT}: {employee.employee_id}"
    email_context = {
        "employee": employee,
        "assigned_assets": assigned_assets,
        "asset_count": len(assigned_assets),
    }
    email_sent = False
    email_recipient = ""

    if user and user.email:
        NotificationService.send_email(
            event=NotificationEvent.EMPLOYEE_OFFBOARDING,
            recipient=user,
            subject=subject,
            template="emails/employee_offboarding.html",
            context=email_context,
        )
        email_sent = True
        email_recipient = user.email
    elif employee.email:
        # Legacy employee records may not have a linked AMS account.
        NotificationEmailService.send(
            recipient_email=employee.email,
            subject=subject,
            template="emails/employee_offboarding.html",
            context=email_context,
            cc=["tz-it@sunking.com", "brenda.nkya@sunking.com"],
        )
        email_sent = True
        email_recipient = employee.email
    else:
        # Ensure IT is notified even when a legacy record has no employee email.
        NotificationEmailService.send(
            recipient_email="tz-it@sunking.com",
            subject=subject,
            template="emails/employee_offboarding.html",
            context=email_context,
            cc=["brenda.nkya@sunking.com"],
        )
        email_sent = True
        email_recipient = "tz-it@sunking.com"

    before = {
        "is_active": employee.is_active,
        "user_is_active": user.is_active if user else None,
        "last_working_date": employee.last_working_date.isoformat(),
    }

    employee.is_active = False
    employee.deactivated_at = now
    employee.updated_at = now
    employee.save(update_fields=["is_active", "deactivated_at", "updated_at"])

    if user and user.is_active:
        user.is_active = False
        user.save(update_fields=["is_active"])

    AuditService.record(
        AuditDTO(
            action="UPDATE",
            entity_type="Employee",
            entity_id=str(employee.pk),
            entity_name=str(employee)[:255],
            actor_id=None,
            actor_name="Celery scheduled offboarding",
            occurred_at=now,
            before=before,
            after={
                "is_active": employee.is_active,
                "user_is_active": user.is_active if user else None,
                "last_working_date": employee.last_working_date.isoformat(),
            },
            metadata={
                "actor": "Celery scheduled offboarding",
                "source": "celery_beat",
                "reason": "employee_exit_date_reached",
                "employee_id": employee.employee_id,
                "email_sent": email_sent,
                "email_recipient": email_recipient,
                "assigned_asset_count": len(assigned_assets),
                "assigned_asset_tags": [
                    assignment.asset.asset_tag for assignment in assigned_assets
                ],
            },
        )
    )

    return True


def due_employee_ids(*, due_date):
    return Employee.objects.filter(
        is_active=True,
        last_working_date__lte=due_date,
    ).values_list("pk", flat=True)
