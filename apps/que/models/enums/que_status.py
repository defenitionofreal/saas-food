from django.db import models


class QueStatus(models.TextChoices):
    """
    Статусы заказа для отображения:
    в обработке;
    принят;
    готовиться;
    готово;
    отменен;
    """
    PROCESSING = "processing", "Processing"
    ACCEPTED = "accepted", "Accepted"
    COOKING = "cooking", "Cooking"
    READY = "ready", "Ready"
    CANCELED = "canceled", "Canceled"
