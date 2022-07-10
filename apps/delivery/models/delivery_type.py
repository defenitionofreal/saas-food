from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

from apps.delivery.models.enums import (DeliveryType,
                                        SaleType,
                                        PaymentType)

User = get_user_model()


def get_absolute_from_percent_and_total(percent, total):
    return round((percent / Decimal('100')) * total)


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

    def get_delivery_sale_type(self):
        return self.sale_type

    def get_delivery_sale_amount(self):
        if self.sale_amount:
            return self.sale_amount
        return 0

    @property
    def is_absolute_discount_type(self):
        return self.get_delivery_sale_type() == SaleType.ABSOLUTE

    @property
    def is_percent_discount_type(self):
        return self.get_delivery_sale_type() == SaleType.PERCENT

    @property
    def has_free_delivery_amount(self):
        return bool(self.free_delivery_amount)

    def get_delivery_discount(self, order_price):
        delivery_sale = self.get_delivery_sale_amount()

        if self.is_absolute_discount_type:
            return delivery_sale

        if self.is_percent_discount_type:
            return get_absolute_from_percent_and_total(delivery_sale, order_price)

        return 0

    def get_delivery_cost(self, order_price):
        min_order_price = self.free_delivery_amount
        if min_order_price and order_price >= min_order_price:
            return 0
        return self.delivery_price
