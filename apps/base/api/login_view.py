from rest_framework import permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from apps.base.serializers import LoginObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginOrganizationTokenView(TokenObtainPairView):
    """ Login endpoint to get JWT token """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginObtainPairSerializer

