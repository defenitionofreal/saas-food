from django.db import models
from django.contrib.auth import get_user_model

from apps.delivery.models.enums import (DeliveryType,
                                        SaleType,
                                        PaymentType)

User = get_user_model()


class Delivery(models.Model):
    """
    Delivery model
    """
    # (required) null because db needed default value to migrate
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True
                             )
    # organization could choose affiliates
    institution = models.ManyToManyField("company.Institution",
                                         related_name="delivery")
    # create 1 of 3 delivery types
    delivery_type = models.CharField(max_length=20,
                                     choices=DeliveryType.choices)
    # multiselect choice
    payment_type = models.CharField(max_length=20,
                                    choices=PaymentType.choices,
                                    default=PaymentType.ONLINE)
    # price for a specific delivery type (optional)
    delivery_price = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         default=0,
                                         blank=True,
                                         null=True)
    # if total bigger than this, delivery is free if delivery_price (optional)
    free_delivery_amount = models.DecimalField(max_digits=10,
                                               decimal_places=2,
                                               default=0,
                                               blank=True,
                                               null=True
                                               )
    # sale for a specific delivery type (optional)
    sale_type = models.CharField(max_length=20,
                                 choices=SaleType.choices,
                                 blank=True,
                                 null=True)
    sale_amount = models.IntegerField(blank=True,
                                      null=True)
    # set minimum total cart price to use delivery (optional)
    min_order_amount = models.IntegerField(blank=True,
                                           null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.delivery_type}"

