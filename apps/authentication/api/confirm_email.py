from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status, permissions)
from rest_framework.exceptions import ValidationError

from apps.authentication.models import VerificationCode
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailConfirmationCodeView(APIView):
    """
    Confirm email by 4 digits from email message.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        email = request.data.get("email", None)
        code = request.data.get("code", None)

        if not email or not code:
            raise ValidationError("Email or code required.")

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("Email not found.")

        verification_code = VerificationCode.objects.filter(
            code=code, email=user.email, is_active=True
        )

        if not verification_code.exists():
            raise ValidationError("Code not found.")

        verification_code.update(is_confirmed=True, is_active=False)
        user.is_email_verified = True
        user.save()

        return Response({"detail": "Email confirmed"},
                        status=status.HTTP_200_OK)
