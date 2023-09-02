from django.db import models
from django.contrib.auth import get_user_model

from apps.delivery.models.enums import (DeliveryType,
                                        SaleType,
                                        PaymentType)

User = get_user_model()


class DeliveryTypeRule(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="delivery"
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=DeliveryType.choices
    )
    payment_types = models.ManyToManyField(
        "payment.PaymentTypeInstitution"
    )
    delivery_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price for a specific delivery type"
    )
    free_delivery_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Delivery is free if total cart is bigger than this "
                  "but if delivery_price is bigger than 0 (optional)"
    )
    sale_type = models.CharField(
        max_length=20,
        choices=SaleType.choices,
        blank=True,
        null=True,
        help_text="Sale for a specific delivery type (optional)"
    )
    sale_amount = models.PositiveIntegerField(
        default=0
    )
    min_order_amount = models.PositiveIntegerField(
        default=0,
        help_text="Minimum total cart price to use delivery (optional)"
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.id}: {self.delivery_type}"

