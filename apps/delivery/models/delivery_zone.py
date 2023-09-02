from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DeliveryZone(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    institutions = models.ManyToManyField(
        "company.Institution"
    )
    title = models.CharField(
        max_length=255
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="If bigger than 0, this price is higher in priority "
                  "than the price for the delivery rule"
    )
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="If bigger than 0, this amount is higher in priority "
                  "than the amount for the delivery rule"
    )
    free_delivery_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="If bigger than 0, this amount is higher in priority "
                  "than the amount for the delivery rule"
    )
    delivery_time = models.PositiveIntegerField(
        default=0,
        help_text="Estimated delivery time in minutes"
    )
    coordinates = models.TextField(
        help_text="Coordinates full array"
    )
    fill_color = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    outline_color = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f'{self.user} -> {self.title}'
