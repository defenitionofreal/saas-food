from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .services.check_auth_code import check_auth_code

User = get_user_model()


class AuthType(str, Enum):
    PHONE = "PHONE"
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"
    BYPASS_ALL = "BYPASS_ALL"  # for testing purposes


class AuthBackend(ModelBackend):
    def authenticate(self, request, auth_type=None, **kwargs):
        if auth_type == AuthType.PHONE:
            phone = kwargs.get("phone")
            code = kwargs.get("code")
            if phone and code:
                user = self._get_user(phone)
                if not user.is_customer:
                    user.is_customer = True
                    user.save()
                return user and self._authenticate(user, code=code)
        if auth_type == AuthType.TELEGRAM:
            # TODO: дописать
            pass
        if auth_type == AuthType.BYPASS_ALL:
            phone = kwargs.get("phone")
            if phone:
                user = self._get_user(phone)
                if not user.is_customer:
                    user.is_customer = True
                    user.save()
                return user

    @staticmethod
    def _get_user(phone):
        if phone:
            try:
                return User.objects.get(phone=phone)
            except User.DoesNotExist:
                pass

    def _authenticate(self, user, code):
        if self._check_code(user, code) and self.user_can_authenticate(user):
            return user

    # @staticmethod
    # def _check_password(user, password):
    #     return password and user.check_password(password)

    @staticmethod
    def _check_code(user, code):
        return code and check_auth_code(user, code)
