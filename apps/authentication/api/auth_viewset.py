from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (exceptions, status, permissions)

from django.contrib.auth import get_user_model

from apps.base.serializers import UserSerializer, LoginObtainPairSerializer

User = get_user_model()


class AuthViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=["post"], url_path="register-organization")
    def register_organization(self, request):
        """
        Registration of an organization user type
        """
        email = request.data.get("email", None)
        phone = request.data.get("phone", None)
        password = request.data.get("password", None)
        password_confirm = request.data.get("password_confirm", None)

        if not email:
            raise exceptions.ValidationError('Enter email')
        if not phone:
            raise exceptions.ValidationError('Enter phone')
        if not password:
            raise exceptions.ValidationError('Enter password')
        if not password_confirm:
            raise exceptions.ValidationError('Confirm password')
        if password != password_confirm:
            raise exceptions.ValidationError('Wrong password')

        organization_user = self.queryset.filter(
            is_customer=False, is_organization=True
        )
        if organization_user.filter(email=email, is_email_verified=True).exists():
            raise exceptions.ValidationError('Email already registered')
        if organization_user.filter(phone=phone, is_sms_verified=True).exists():
            raise exceptions.ValidationError('Phone already registered')

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_organization=True)

        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="login-organization")
    def login_organization(self, request):
        """
        Login valid organization user type and return access token
        """
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email or not password:
            raise exceptions.ValidationError("All fields are required.")

        user = self.queryset.filter(email=email).first()
        if (user and user.check_password(password)) and (user.is_organization and user.is_active):
            serializer = LoginObtainPairSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data.get("access", None)
            refresh = serializer.validated_data.get("refresh", None)

            if access:
                response = Response({"access": access}, status=200)
                response.set_cookie('refresh',
                                    refresh,
                                    httponly=True,
                                    samesite="None",
                                    secure="false")
                return response

        return Response({"detail": "Check data"},
                        status=status.HTTP_400_BAD_REQUEST)

    # CUSTOMER

    # @action(detail=False, methods=["post"], url_path="register-customer")
    # def register_customer(self, request):
    #     """
    #     Registration of a customer user type
    #     """
    #     phone = request.data.get("phone", None)
    #     password = request.data.get("password", None)
    #     password_confirm = request.data.get("password_confirm", None)
    #
    #     if not phone:
    #         raise exceptions.ValidationError('Enter phone')
    #     if not password:
    #         raise exceptions.ValidationError('Enter password')
    #     if not password_confirm:
    #         raise exceptions.ValidationError('Confirm password')
    #     if password != password_confirm:
    #         raise exceptions.ValidationError('Wrong password')
    #
    #     customer_user = self.queryset.filter(
    #         is_customer=True, is_organization=False
    #     )
    #     if customer_user.filter(phone=phone, is_sms_verified=True).exists():
    #         raise exceptions.ValidationError('Phone already registered')
    #
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(is_organization=True)
    #
    #     return Response(serializer.data, status.HTTP_201_CREATED)



