from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.base.serializers import LoginObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginOrganizationTokenView(TokenObtainPairView):
    """ Login endpoint to get JWT token """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access is not None:
            response = Response({"access": access}, status=200)
            response.set_cookie('refresh', refresh,
                                httponly=True,
                                samesite="Lax")
            return response
        return Response({"Error": "Something went wrong"}, status=400)

