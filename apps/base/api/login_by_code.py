from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.base.backends import AuthType
from apps.base.serializers import AuthPhoneSerializer, AuthSendCodeSerializer

from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class AuthCustomerAPIView(APIView):
    """
    Authentication for a is_customer via phone
    """
    def post(self, request):
        data: dict = request.data
        auth_type = data.get("auth_type", None)
        if auth_type == AuthType.PHONE:
            serializer = AuthPhoneSerializer(data=data)
            if serializer.is_valid():

                user = authenticate(request,
                                    auth_type=AuthType.PHONE,
                                    **serializer.validated_data)
                if user:
                    login(request, user)
                    response = Response(self.get_tokens_for_user(user),
                                        status=status.HTTP_200_OK)
                else:
                    response = Response(
                        {"errors": "Неверный код! Введите еще раз"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            return response
        elif auth_type == AuthType.TELEGRAM:
            # TODO: дописать код под телеграм бота
            pass
        elif auth_type == AuthType.BYPASS_ALL:
            serializer = AuthSendCodeSerializer(data=data)
            if serializer.is_valid():
                user = authenticate(request,
                                    auth_type=AuthType.BYPASS_ALL,
                                    **serializer.validated_data)
                if user:
                    login(request, user)
                    response = Response(self.get_tokens_for_user(user),
                                        status=status.HTTP_200_OK)
                else:
                    response = Response(
                        {"errors": "Something went wrong"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            return response
        else:
            return Response({"errors": "Несуществующий тип аунтефикации"},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh),
                'access': str(refresh.access_token)}
