from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user_agents import parse
from ipware import get_client_ip

from apps.base.serializers import AuthSendCodeSerializer
from apps.base.services.send_auth_code import send_auth_code
from apps.base.models import AuthCode
from django.contrib.auth import get_user_model


class SendAuthCodeView(APIView):

    def post(self, request):
        client_ip, _ = get_client_ip(request)
        if not self._user_agent_is_valid(request):
            response = Response({"errors": "Not provided user agent"},
                                status=status.HTTP_403_FORBIDDEN)
        elif not client_ip:
            response = Response({"errors": "Not provided user ip address"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            response = self._send_authentication_code(request)
        return response

    @staticmethod
    def _user_agent_is_valid(request):
        """
        Check that request was by a real user and not a bot
        """
        user_agent = request.META.get("HTTP_USER_AGENT")
        if user_agent:
            is_valid = not parse(user_agent).is_bot
        else:
            is_valid = False
        return is_valid

    def _send_authentication_code(self, request):
        serializer = AuthSendCodeSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            phone = str(phone)
            phones_count_prefix = self._build_phones_count_prefix(request)

            try:
                resending_time = send_auth_code(phone, phones_count_prefix)
                # code для просмотра кода в режиме разработке,
                # так это поле в смс приходит
                # user = get_user_model().objects.get(phone=phone)
                # code = AuthCode.objects.filter(user=user).order_by(
                #     '-created_at').first()
                # print("_send_authentication_code", code)
                response = Response({**serializer.data,
                                     "resending_time": resending_time})
            except Exception as e:
                response = Response(
                    {
                        "errors": f"Не удалось отправить код на {phone} {e}"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return response

    @staticmethod
    def _build_phones_count_prefix(request):
        client_ip, _ = get_client_ip(request)
        user_agent = request.META["HTTP_USER_AGENT"].replace(" ", "")
        return f"USED_{client_ip}_{user_agent}"
