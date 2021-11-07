from django.db import models


class SaleType(models.TextChoices):
    ABSOLUTE = "absolute", "Absolute"  # в рублях
    PERCENT = "percent", "Percent"  # в процентах