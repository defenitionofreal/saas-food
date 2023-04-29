from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status, permissions)
from rest_framework.exceptions import ValidationError

from apps.authentication.models import VerificationCode
from apps.base.models import MessageLog
from apps.base.models.enums import LogTypes, LogStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneConfirmationCodeView(APIView):
    """
    Confirm phone by 4 digits from sms message.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        phone = request.data.get("phone", None)
        code = request.data.get("code", None)

        if not phone or not code:
            raise ValidationError("Phone and code required.")

        user = User.objects.filter(phone=phone).first()

        if not user:
            raise ValidationError("User not found.")

        verification_code = VerificationCode.objects.filter(
            code=code, phone=user.phone, is_active=True
        )

        if not verification_code.exists():
            raise ValidationError("Code not found.")

        verification_code_instance = verification_code.first()
        verification_code_instance.is_confirmed = True
        verification_code_instance.is_active = False
        verification_code_instance.save()

        user.is_sms_verified = True
        user.save()

        VerificationCode.objects.filter(phone=user.phone).exclude(
            id=verification_code_instance.id).update(is_active=False)

        MessageLog.objects.create(
            type=LogTypes.CONFIRM_PHONE,
            status=LogStatus.SUCCESS,
            content=f"Phone {str(user.phone)} confirmed."
        )

        return Response({"detail": "Phone confirmed"},
                        status=status.HTTP_200_OK)
