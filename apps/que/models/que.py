from django.db import models
from apps.que.models.enums import QueStatus


class Que(models.Model):
    """
    Queue model for order status
    """
    order = models.ForeignKey("order.Cart", on_delete=models.CASCADE, related_name="que")
    number = models.CharField(max_length=4)  # генерируемы номерок типо B523
    status = models.CharField(max_length=20, choices=QueStatus.choices)
