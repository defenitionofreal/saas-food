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
                             "message": "Код отправлен на почту"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))

#
# class EmailConfirmationCodeView(APIView):
#     """
#     Подтверждения кода для авторизации на сайте, принимает email и code.
#     Токен устанавливается в куки
#     """
#
#     def post(self, request):
#         email = request.data.get('email')
#         code = request.data.get('code')
#
#         user = User.objects.filter(email=email).first()
#         if not user:
#             raise ValidationError("Пользователь с указанным email не найден.")
#
#         # default user logic
#         default_user = get_default_user(code=code, email=email)
#         if default_user:
#             token, _ = Token.objects.get_or_create(user=default_user)
#             response = Response({'user': default_user.id})
#             response.set_cookie("token", token.key, httponly=True, secure=True)
#             return response
#
#         verification_code = VerificationCode.objects.filter(
#             code=code, email=user.email, is_active=True
#         )
#
#         if verification_code.exists() is False:
#             raise ValidationError("Подтвердить почту не удалось.")
#
#         verification_code.update(is_confirmed=True, is_active=False)
#         user.confirmationed_email = True
#         user.save()
#
#         token, _ = Token.objects.get_or_create(user=user)
#         response = Response({'user': user.id})
#         response.set_cookie('token', token.key, httponly=True, secure=True)
#
#         return response
