from django.db import models


class OrderStatus(models.TextChoices):
    """
    Order status for basic conditions and not
     * if delivery type is pick up or take away:
        - customer see statuses: PLACED, ACCEPTED, COOKING, READY
        - GIVEN_AWAY status is for an organization mark
    * if delivery status is by courier:
       - customer see statuses: PLACED, ACCEPTED, COOKING, READY, ON_THE_WAY,
         DELIVERED
    """
    DRAFT = "draft", "Draft"
    # basic
    PLACED = "placed", "Placed"  # размещен
    ACCEPTED = "accepted", "Accepted"  # принят
    COOKING = "cooking", "Cooking"  # готовится
    READY = "ready", "Ready"  # готово
    # courier
    ON_THE_WAY = "on the way", "On the way"  # в пути
    DELIVERED = "delivered", "Delivered"  # доставлен
    # pick up / indoor
    GIVEN_AWAY = "given away", "Given away"  # отдан

    CANCELED = "cancel", "Cancel"
