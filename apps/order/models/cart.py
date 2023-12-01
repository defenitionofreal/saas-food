from typing import Optional

from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from apps.delivery.models import DeliveryZone, CartDeliveryInfo
from apps.order.models import Bonus
from apps.order.models.enums.order_status import OrderStatus
from apps.order.services.coupon_helper import CouponHelper


from apps.delivery.models.enums import DeliveryType
from apps.payment.models.enums import PaymentType

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
from decimal import Decimal


import json

User = get_user_model()


class Cart(models.Model):
    """
    A model that contains data for a shopping cart.
    Minimum amount at cart (if added)
    delivery cost (if added) ?! or in order model?
    promo code (coupon) for sale
    add bonus points to a customer profile or he could spend his points
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="cart_institution")
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='cart_customer',
                                 null=True, blank=True)
    confirmed_date = models.DateTimeField(blank=True,
                                          null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sales part
    promo_code = models.ForeignKey("order.PromoCode",
                                   on_delete=models.SET_NULL,
                                   related_name="cart_promo_code",
                                   null=True,
                                   blank=True)
    customer_bonus = models.PositiveIntegerField(default=0)
    # order min amount rule
    min_amount = models.PositiveIntegerField(default=0)

    # user info part
    name = models.CharField(max_length=255, default="имя")
    phone = PhoneNumberField(blank=True,
                             null=True)
    email = models.EmailField(blank=True,
                              null=True)
    comment = models.TextField(max_length=1000, blank=True)
    payment_type = models.CharField(max_length=20,
                                    choices=PaymentType.choices,
                                    default=PaymentType.ONLINE)
    # order main stuff
    code = models.CharField(max_length=5,
                            blank=True,
                            null=True)
    status = models.CharField(max_length=10,
                              choices=OrderStatus.choices,
                              default=OrderStatus.DRAFT)
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)
    # paid field should be for an online payment only?
    paid = models.BooleanField(default=False)

    @property
    def delivery(self) -> Optional[CartDeliveryInfo]:
        return self.cartdeliveryinfo_set.first()

    @property
    def get_delivery_price(self) -> Decimal:
        return self.delivery.delivery_price if self.delivery else Decimal("0")

    @property
    def get_free_delivery_amount(self) -> Decimal:
        return self.delivery.free_delivery_amount if self.delivery else Decimal("0")

    @property
    def get_min_delivery_order_amount(self) -> int:
        return self.delivery.min_delivery_order_amount if self.delivery else 0

    @property
    def get_delivery_sale(self) -> Decimal:
        return self.delivery.delivery_sale if self.delivery else Decimal("0")

    @property
    def get_total_cart(self) -> int:
        total = sum(
            [i.get_total_item_price for i in self.products_cart.all()]
        ) if self.products_cart.all() else 0
        return total

    @property
    def get_promo_code_sale(self) -> int:
        if self.promo_code and self.customer:
            helper = CouponHelper(self.promo_code, self, self.customer)
            return helper.final_sale()[0]
        return 0

    @property
    def get_final_sale(self) -> float:
        """
        Sale includes coupon and bonus amount if bonus rule exists
        """
        promo_code_sale = self.get_promo_code_sale
        customer_bonus = self.customer_bonus
        has_coupon_bonus_rule = Bonus.objects.filter(
            institutions=self.institution,
            is_active=True,
            is_promo_code=True
        ).exists()

        sale = promo_code_sale + customer_bonus if customer_bonus and has_coupon_bonus_rule else promo_code_sale
        if customer_bonus and not self.promo_code:
            sale = customer_bonus

        return sale

    @property
    def get_total_with_sale(self) -> float:
        """ общая скидка с промокодом и бонусами если есть """
        # todo: по сути бессмыслица, удалить это поле и там где оно использется написать total - final_price
        return self.get_total_cart - self.get_final_sale

    @property
    def get_bonus_accrual(self):
        """ max accrual amount """
        bonus = Bonus.objects.get(institutions=self.institution)
        total_accrual = 0
        if bonus.is_active:
            if self.promo_code:
                total_accrual = round((bonus.accrual / Decimal('100')) * (self.get_total_cart - self.get_promo_code_sale))
            else:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart)
        return total_accrual

    @property
    def get_bonus_write_off(self):
        """ max write off amount """
        bonus = Bonus.objects.get(institutions=self.institution)
        total_write_off = 0
        if bonus.is_active:
            if self.promo_code:
                total_write_off = round((bonus.write_off / Decimal('100')) * (self.get_total_cart - self.get_promo_code_sale))
            else:
                total_write_off = round((bonus.write_off / Decimal('100')) * self.get_total_cart)
        return total_write_off

    @property
    def final_price(self) -> float:
        """ """
        # TODO: CHECK THAT SALE NOT MORE THAN PRICE AMOUNT AFTER ALL (LIMIT BONUS WRITE OFF RULE?!)
        delivery_sale = self.delivery.delivery_sale if self.delivery else 0
        delivery_price = self.delivery.final_delivery_price if self.delivery else 0
        total = (self.get_total_with_sale + delivery_price) - delivery_sale
        return Decimal("1") if total == 0 else total

    def __str__(self):
        return f'{self.id}: {self.institution}, {self.customer}, ' \
               f'{self.get_total_cart}'
