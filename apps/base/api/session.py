from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from apps.base.serializers import SessionSerializer

User = get_user_model()


class SessionAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if not request.session.session_key and not any(
                agent in user_agent for agent in ['curl', 'yandexbot']):
            request.session.save()

        data = {"session_id": request.session.session_key,
                "max_age": request.session.get_expiry_age()}

        serializer = SessionSerializer(data, many=False, read_only=True)

        return Response(serializer.data)

