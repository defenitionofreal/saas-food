from django.db import models
from django.contrib.auth import get_user_model
from apps.que.models.enums import QueStatus

User = get_user_model()


class Que(models.Model):
    """
    Queue model for order status
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="que")
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="que")
    number = models.CharField(max_length=4)  # генерируемы номерок типо B523
    status = models.CharField(max_length=20, choices=QueStatus.choices)
