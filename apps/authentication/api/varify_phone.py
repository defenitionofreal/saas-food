from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status, permissions)
from rest_framework.exceptions import (ValidationError, APIException)

from apps.base.models import MessageLog
from apps.base.models.enums import (LogTypes, LogStatus)
from apps.authentication.models import VerificationCode
from apps.authentication.services.create_verification_code import create_verification_code
from apps.sms.services.sms_base_class import (SmsBaseHelper, SmsProvider)


from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class PhoneVerificationCodeView(APIView):
    """
    send email with 4 digits code
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        phone = str(request.data.get('phone'))
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise ValidationError({"detail": "Phone not found."})

        time = timezone.now() - timedelta(minutes=30)
        verification_qs = VerificationCode.objects.filter(
            phone=str(user.phone), created_at__gte=time
        )
        if verification_qs.count() >= 3:
            raise ValidationError({"detail": "Try again after 30 minutes."})

        try:
            verification, _ = VerificationCode.objects.get_or_create(
                phone=str(user.phone),
                code=create_verification_code()
            )

            msg = f"Verification code: {verification.code}"

            helper = SmsBaseHelper(SmsProvider.TWILIO)
            result = helper.send_sms(str(user.phone), msg)
            if result:
                MessageLog.objects.create(
                    type=LogTypes.VERIFY_PHONE,
                    status=LogStatus.SUCCESS,
                    content=f"Phone {str(user.phone)} verification code:\n {verification.code}"
                )
                return Response({"detail": "Code successfully send"},
                                status=status.HTTP_200_OK)

            MessageLog.objects.create(
                type=LogTypes.VERIFY_PHONE,
                status=LogStatus.ERROR,
                content=f"Phone {user.phone} verification code error:\n"
            )
            return Response({"detail": "sms server error"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise APIException(str(e))
