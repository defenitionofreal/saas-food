from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CartDeliveryInfo(models.Model):
    cart = models.ForeignKey(
        "order.Cart",
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        "delivery.DeliveryTypeRule",
        on_delete=models.CASCADE
    )
    customer_address = models.ForeignKey(
        "delivery.CustomerAddress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="address filled if delivery type is courier"
    )
    institution_address = models.ForeignKey(
        "delivery.InstitutionAddress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="address filled if delivery type is pickup or indoor"
    )
    delivery_date = models.DateField(
        blank=True,
        null=True
    )
    delivery_time = models.TimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.id}: {self.type}"
