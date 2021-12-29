from django.db import models

from apps.delivery.models.enums import (DeliveryType,
                                        SaleType,
                                        PaymentType)


class Delivery(models.Model):
    """
    Delivery model
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="delivery")
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.ONLINE)
    sale_type = models.CharField(max_length=20, choices=SaleType.choices)
    sale_amount = models.IntegerField()
    date_when = models.DateTimeField()

    def __str__(self):
        return self.institution

