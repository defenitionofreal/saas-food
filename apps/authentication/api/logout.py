from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        del response["Token"]

        # delete cart session
        session = self.request.session
        if session:
            if settings.CART_SESSION_ID in session:
                del session[settings.CART_SESSION_ID]
            session.flush()

        response.data = {
            "detail": "success"
        }
        return response
