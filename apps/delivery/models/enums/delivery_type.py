from django.db import models


class DeliveryType(models.TextChoices):
    PICKUP = "pickup", "Pickup"  # с собой
    COURIER = "courier", "Courier"  # доставка
    INDOOR = "indoor", "Indoor"  # в зале
