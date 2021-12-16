from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.base.authentication import JWTAuthentication

from django.contrib.auth import get_user_model

User = get_user_model()


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            "message": "success"
        }
        return response
