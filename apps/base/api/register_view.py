from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status, permissions

from apps.base.serializers import UserSerializer


class RegisterAPIView(APIView):
    """
    Register organizations (not customers!)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        if data['email'] == '' or data['email'] is None:
            raise exceptions.APIException('Некорректная почта')
        if data['phone'] == '' or data['phone'] is None:
            raise exceptions.APIException('Некорректный телефон')
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Неверный пароль')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
