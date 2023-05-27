import datetime
import uuid
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (exceptions, status, permissions)
from rest_framework_simplejwt.tokens import (
    BlacklistedToken, OutstandingToken, RefreshToken
)

from django.contrib.auth import get_user_model

from apps.base.serializers import UserSerializer
from apps.base.models import MessageLog
from apps.base.models.enums import (LogTypes, LogStatus)

from apps.authentication.serializers import LoginObtainPairSerializer
from apps.authentication.models import VerificationCode
from apps.authentication.services.create_verification_code import create_verification_code
from apps.sms.services.sms_by_organization import SmsOrganizationHelper
from apps.company.models import Institution

import re

User = get_user_model()
logger = logging.getLogger(__name__)


def validate_contact_input(input_str):
    """
    Validate input_str if its an email or a phone.
    """
    # Define regular expressions for email and phone number
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
    # Match the input string against the regular expressions
    if re.match(email_regex, input_str):
        return "email"
    elif re.match(phone_regex, input_str):
        return "phone"
    else:
        return None


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

        logger.info("Organization successfully registered.")

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
                logger.info("Organization successfully logged in.")
                return response

        return Response({"detail": "Check data"},
                        status=status.HTTP_400_BAD_REQUEST)

    # CUSTOMER

    @action(detail=False, methods=["post"],
            url_path="(?P<institution_domain>[^/.]+)/customer-authentication")
    def customer_authentication(self, request, institution_domain=None):
        """
        Auth system for a customer.

        Detects contact field if its email or phone.
        Email auth is set by default if organization dont have a sms provider.
        So if its email auth and no user found with this email, we register him.
        If user found we check at first that email is confirmed and if it is,
        we login him.

        If contact field is phone, we check if organization has sms provider.
        If no user found with this phone number. we register him with a draft
        email. If user found we check at firm is phone is confirmed if not, we
        send code by sms with organization credentials through there provider.
        If phone is confirmed, we login user.
        """
        response = Response({"detail": ""}, status=status.HTTP_400_BAD_REQUEST)
        contact_field = request.data.get("contact", None)
        password = request.data.get("password", None)
        institution = Institution.objects.get(domain=institution_domain)

        if not contact_field or not password:
            raise exceptions.ValidationError("Contact and password fields are required.")

        validated_contact = validate_contact_input(contact_field)

        if not validated_contact:
            raise exceptions.ValidationError("Wrong value at contact field.")

        user_qs = self.queryset.filter(is_customer=True, is_organization=False)

        if validated_contact == "email":
            request.data["email"] = contact_field
            request.data["phone"] = None
            request.data["password"] = password
            request.data["password_confirm"] = password

            user = user_qs.filter(email=contact_field).first()

            if not user:
                # customer registration via email
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(is_customer=True)
                logger.info("Customer successfully registered by email.")
                response = Response(serializer.data, status.HTTP_201_CREATED)
            else:
                # customer login via email
                if not user.check_password(password):
                    response = Response({"detail": "Wrong email or password"}, status=400)

                elif not user.is_customer or not user.is_active:
                    response = Response({"detail": "Your profile unavailable. Contact with support."}, status=400)

                elif not user.is_email_verified:
                    response = Response({"detail": "Verify your email."},
                                        status=400)
                else:
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
                        logger.info("Customer successfully logged in by email.")

        if validated_contact == "phone":
            # todo: Может разрешить авторизацию по телефону без подтверждения
            #  или если у организации нету смс провайдера, просто если есть,
            #  то тогда просить подтвердить?! Пример пиццерия "робертиньё".
            sms_helper = SmsOrganizationHelper(institution.id)
            sms_provider = sms_helper.get_sms_provider_type()
            if not sms_provider:
                return Response({"detail": "no sms provider found"}, status=status.HTTP_400_BAD_REQUEST)

            request.data["phone"] = contact_field
            request.data["password"] = password
            request.data["password_confirm"] = password
            user = user_qs.filter(phone=contact_field).first()
            if not user:
                # регистрирую
                request.data["email"] = f"{contact_field}@draft.ru"
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(is_customer=True)
                logger.info("Customer successfully registered by phone.")
                response = Response(serializer.data, status.HTTP_201_CREATED)
            else:
                # авторизовываю
                if not user.check_password(password):
                    response = Response({"detail": "Wrong email or password"}, status=400)

                elif not user.is_customer or not user.is_active:
                    response = Response({"detail": "Your profile unavailable. Contact with support."}, status=400)

                elif not user.is_sms_verified:
                    try:
                        verification, _ = VerificationCode.objects.get_or_create(
                            phone=str(user.phone),
                            code=create_verification_code()
                        )
                        msg = f"Verification code: {verification.code}"
                        is_sent = sms_helper.send_sms(to_phone=str(user.phone), message=msg)
                        if is_sent:
                            logger.info("Customer successfully sent verification code.")
                            response = Response({"detail": "Verification code is sent."}, status=status.HTTP_200_OK)
                    except Exception as e:
                        logger.error(f"Customer phone auth error {e}")
                        response = Response({"detail": e}, status=400)

                else:
                    request.data["email"] = user.email
                    serializer = LoginObtainPairSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    access = serializer.validated_data.get("access", None)
                    refresh = serializer.validated_data.get("refresh", None)
                    if access:
                        res = Response({"access": access}, status=200)
                        res.set_cookie('refresh',
                                       refresh,
                                       httponly=True,
                                       samesite="None",
                                       secure="false")
                        logger.info("Customer successfully logged in by phone.")
                        response = res

        return response

    @action(detail=False, methods=["post"],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        Base logout for organizations and customer.
        """
        access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        outstanding_token = OutstandingToken.objects.filter(token=access_token).first()
        if not outstanding_token:
            while True:
                jti = str(uuid.uuid4())
                if not OutstandingToken.objects.filter(jti=jti).exists():
                    break
            outstanding_token, _ = OutstandingToken.objects.get_or_create(
                user=self.request.user,
                jti=jti,
                token=access_token,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now()
            )

        black_token, created = BlacklistedToken.objects.get_or_create(token=outstanding_token)
        if not created:
            logger.warning(f"Logout invalid token by user {self.request.user.id}")
            return Response({"detail": "Invalid token. Already at black list."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Invalidate Refresh Token
        refresh_token = request.data.get('refresh', None)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f"Black list refresh token by user {self.request.user.id}")
            except Exception as e:
                logger.error(f"Black list refresh token error by user {self.request.user.id}: {e}")
                return Response({'detail': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        # # delete cart session
        # session = self.request.session
        # if session:
        #     if settings.CART_SESSION_ID in session:
        #         del session[settings.CART_SESSION_ID]
        #     session.flush()

        logger.info(f"Logout successfully by user {self.request.user.id}")

        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)
