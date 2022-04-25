from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from apps.base.serializers import LoginObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginOrganizationTokenView(TokenObtainPairView):
    """ Login endpoint to get JWT token and user info"""
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access is not None:
            response = Response({"access": access},
                                status=200)
            response.set_cookie('refresh',
                                refresh,
                                httponly=True,
                                samesite="None",
                                secure="false")
            return response
        return Response({"Error": "Something went wrong"}, status=400)

    # @staticmethod
    # def get_user_from_access_token(access_token_str):
    #     access_token_obj = AccessToken(access_token_str)
    #     user_id = access_token_obj['user_id']
    #     user = User.objects.get(id=user_id)
    #     content = {"id": user.id,
    #                "phone": str(user.phone),
    #                "email": user.email,
    #                "username": user.username,
    #                "first_name": user.first_name,
    #                "middle_name": user.middle_name,
    #                "last_name": user.last_name}
    #     return content
