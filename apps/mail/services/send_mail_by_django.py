import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()
logger = logging.getLogger(__name__)


def send_mail_by_django(category=None, context=None):
    subject = None
    text = None
    template = None
    user_id = context.get('user_id')
    user = User.objects.get(id=user_id)

    if category == 'email-verification':
        subject = f'Verification code'
        text = f'Verification code'
        template = 'email_verification.html'
    else:
        raise ValueError("Error")

    msg_html = render_to_string(template, context)

    if all([user, subject, msg_html]):
        send_mail(
            subject=subject,
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=msg_html,
            fail_silently=False
        )
        logger.info("Email sent successfully.")
