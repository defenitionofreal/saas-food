from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.base.authentication import JWTAuthentication

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie(key='jwt')

        # delete cart session
        session = self.request.session
        if session:
            if settings.CART_SESSION_ID in session:
                del session[settings.CART_SESSION_ID]
            session.flush()

        response.data = {
            "message": "success"
        }
        return response
