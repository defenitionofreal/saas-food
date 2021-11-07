from django.db import models


class WeightUnit(models.TextChoices):
    """
    WeightUnit
    """
    LITER = "liter", "Liter"
    MILLILITER = "milliliter", "Milliliter"
    GRAM = "gram", "Gram"
    KILOGRAM = "kilogram", "Kilogram"
