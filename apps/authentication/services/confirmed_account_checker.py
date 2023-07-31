from rest_framework.exceptions import ValidationError


class ConfirmedAccountChecker:

    def __init__(self, user):
        self.user = user

    def _is_phone_confirmed(self):
        user = self.user
        if not user.is_sms_verified:
            raise ValidationError({"detail": "Phone is not confirmed."})

    def _is_email_confirmed(self):
        user = self.user
        if not user.is_email_verified:
            raise ValidationError({"detail": "Email is not confirmed."})

    def _is_customer(self):
        user = self.user
        if not user.is_customer:
            raise ValidationError({"detail": "User is not a customer."})

    def _is_organization(self):
        user = self.user
        if not user.is_organization:
            raise ValidationError({"detail": "User is not a organization."})

    def is_confirmed(self):
        self._is_email_confirmed()
        self._is_phone_confirmed()
        return True

    def is_customer(self):
        self._is_customer()
        return True

    def is_organization(self):
        self._is_organization()
        return True
