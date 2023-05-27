from django.db import models


class LogTypes(models.IntegerChoices):
    VERIFY_EMAIL = 0, "Email verification"
    CONFIRM_EMAIL = 1, "Email confirmation"
    VERIFY_PHONE = 3, "Phone verification"
    CONFIRM_PHONE = 4, "Phone confirmation"

    REGISTRATION_ORGANIZATION = 5, "Registration organization"
    LOGIN_ORGANIZATION = 6, "Login organization"
    REGISTRATION_CUSTOMER = 7, "Registration customer"
    LOGIN_CUSTOMER = 8, "Login customer"
    # todo: much more
