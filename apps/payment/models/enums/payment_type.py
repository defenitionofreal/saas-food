from django.db import models


class PaymentType(models.TextChoices):
    CASH = "cash", "Cash"  # наличными
    CARD = "card", "Card"  # картой при получении
    ONLINE = "online", "Online"  # картой онлайн
