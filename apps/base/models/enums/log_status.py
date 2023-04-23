from django.db import models


class LogStatus(models.IntegerChoices):
    SUCCESS = 0, "success"
    ERROR = 1, "error"
    # todo: much more
