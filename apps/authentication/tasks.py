from celery import shared_task

from django.contrib.auth import get_user_model

from apps.base.models import MessageLog
from apps.base.models.enums import (LogTypes, LogStatus)
from apps.mail.services.send_mail_by_django import send_mail_by_django
from apps.authentication.models import VerificationCode
from apps.authentication.services.create_verification_code import create_verification_code

User = get_user_model()


@shared_task
def send_email_verification_code_task(email: str):
    """
    Verification code to confirm accounts email.
    """

    user = User.objects.filter(email=email).first()
    if not user:
        return

    verification, _ = VerificationCode.objects.get_or_create(
        email=user.email,
        code=create_verification_code()
    )
    try:
        send_mail_by_django(category="email-verification",
                            context={"code": verification.code,
                                     "user_id": user.id})
        MessageLog.objects.create(
            type=LogTypes.VERIFY_EMAIL,
            status=LogStatus.SUCCESS,
            content=f"Email {user.email} verification code:\n{verification.code}"
        )
    except Exception as e:

        MessageLog.objects.create(
            type=LogTypes.VERIFY_EMAIL,
            status=LogStatus.ERROR,
            content=f"Error email {user.email} verification code:\n{e}"
        )
