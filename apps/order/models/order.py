from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    """
    Order model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    full_name = models.CharField(max_length=255)
    phone = models.CharField()  # phone field change
    city = models.CharField()
    address = models.CharField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(max_length=1000, blank=True)
    date_delivery = models.DateTimeField(blank=True)  # время доставки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # promocode