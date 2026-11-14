import logging

from celery import shared_task
from django.utils import timezone

from employees.services.offboarding import (
    due_employee_ids,
    offboard_employee_for_exit,
)


logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def enqueue_due_employee_offboardings():
    """Queue every active employee whose exit date has arrived."""
    due_date = timezone.localdate()
    employee_ids = list(due_employee_ids(due_date=due_date))

    for employee_id in employee_ids:
        process_due_employee_offboarding.delay(str(employee_id))

    logger.info(
        "Queued %s employee offboarding task(s) for %s",
        len(employee_ids),
        due_date,
    )
    return len(employee_ids)


@shared_task(
    bind=True,
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=3600,
    retry_jitter=True,
    max_retries=8,
)
def process_due_employee_offboarding(self, employee_id):
    """Send the notice and deactivate one due employee and account."""
    return offboard_employee_for_exit(
        employee_id,
        due_date=timezone.localdate(),
    )
