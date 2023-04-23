from django.db import models


class LogTypes(models.IntegerChoices):
    VERIFY_EMAIL = 0, "Email verification"
    CONFIRM_EMAIL = 1, "Email confirmation"
    VERIFY_PHONE = 3, "Phone verification"
    CONFIRM_PHONE = 4, "Phone confirmation"
    # todo: much more
