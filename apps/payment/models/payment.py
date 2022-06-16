from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    """
    Payment model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment")
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="payment")
    system = models.CharField(max_length=255)  # здесь нужен Choices с системами или что?
    payment_date = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
