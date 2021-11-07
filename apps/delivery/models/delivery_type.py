from django.db import models

from apps.delivery.models.enums import (DeliveryType,
                                        SaleType)


class Delivery(models.Model):
    """
    Delivery model
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="delivery")
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices)
    by_card = models.BooleanField(default=False)
    by_cash = models.BooleanField(default=False)
    by_card_online = models.BooleanField(default=False)
    sale_type = models.CharField(max_length=20, choices=SaleType.choices)
    sale_amount = models.IntegerField()
    date_when = models.DateTimeField()

    def __str__(self):
        return self.institution


# сделать ЗОНУ ДОСТАВКИ  DeliveryZone
