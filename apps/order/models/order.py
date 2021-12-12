from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    """
    Order model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)  # phone field change
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(max_length=1000, blank=True)
    date_delivery = models.DateTimeField(blank=True,
                                         null=True)  # время доставки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.ForeignKey("order.PromoCode", on_delete=models.CASCADE,
                                   related_name="order", null=True, blank=True)
