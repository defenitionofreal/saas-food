from django.db import models


class DeliveryType(models.TextChoices):
    PICKUP = "pickup", "Pickup"  # самовывоз
    TAKEAWAY = "takeaway", "Takeaway"  # с собой
    INSTITUTION = "institution", "Institution"  # в заведение
