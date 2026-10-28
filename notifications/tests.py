from unittest.mock import Mock, patch

from django.core import mail
from django.test import SimpleTestCase, override_settings

from core.notifications.email import NotificationEmailService
from core.notifications.enums import NotificationEvent
from core.notifications.service import NotificationService


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotificationEmailServiceTests(SimpleTestCase):

	@patch("core.notifications.email.render_to_string", return_value="<p>Notice</p>")
	def test_email_defaults_to_it_cc_only(self, render_to_string):
		NotificationEmailService.send(
			recipient_email="employee@example.com",
			subject="Assignment",
			template="emails/asset_assigned.html",
		)

		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].cc, ["tz-it@sunking.com"])

	@patch("core.notifications.service.NotificationEmailService.send")
	@patch("core.notifications.service.Notification.objects.create")
	def test_offboarding_email_copies_brenda(self, create_notification, send_email):
		recipient = Mock(email="employee@example.com")

		NotificationService.send_email(
			event=NotificationEvent.EMPLOYEE_OFFBOARDING,
			recipient=recipient,
			subject="Offboarding",
			template="emails/employee_offboarding.html",
		)

		self.assertEqual(
			send_email.call_args.kwargs["cc"],
			["tz-it@sunking.com", "brenda.nkya@sunking.com"],
		)

	@patch("core.notifications.service.NotificationEmailService.send")
	@patch("core.notifications.service.Notification.objects.create")
	def test_assignment_email_does_not_copy_brenda(self, create_notification, send_email):
		recipient = Mock(email="employee@example.com")

		NotificationService.send_email(
			event=NotificationEvent.ASSET_ASSIGNED,
			recipient=recipient,
			subject="Assignment",
			template="emails/asset_assigned.html",
		)

		self.assertEqual(
			send_email.call_args.kwargs["cc"],
			["tz-it@sunking.com"],
		)
