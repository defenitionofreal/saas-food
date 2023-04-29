from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status, permissions)
from rest_framework.exceptions import (ValidationError, APIException)

from apps.authentication.models import VerificationCode
from apps.authentication.tasks import send_email_verification_code_task

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class EmailVerificationCodeView(APIView):
    """
    send email with 4 digits code
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):

        email = str(request.data.get('email')).lower()
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("Email not found.")

        time = timezone.now() - timedelta(minutes=30)
        verification_qs = VerificationCode.objects.filter(
            email=str(user.email), created_at__gte=time
        )
        if verification_qs.count() >= 3:
            raise ValidationError("Try again after 30 minutes.")

        try:
            send_email_verification_code_task.delay(email=str(user.email))
            return Response({"status": "success",
                             "message": "Code successfully send"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))
