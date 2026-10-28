from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class NotificationEmailService:

    @staticmethod
    def send(
        *,
        recipient_email,
        subject,
        template,
        context=None,
        cc=None,
        attachments=None,
    ):
        context = context or {}

        html_content = render_to_string(template, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=(
                "Please view this email "
                "in an HTML-compatible email client."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
            cc=cc if cc is not None else ["tz-it@sunking.com"],
        )

        email.attach_alternative(html_content, "text/html")

        for attachment in attachments or []:
            filename, content, mimetype = attachment
            email.attach(filename, content, mimetype)

        email.send(fail_silently=False)