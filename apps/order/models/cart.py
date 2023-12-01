from typing import Optional

from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from apps.delivery.models import CartDeliveryInfo
from apps.order.models import Bonus
from apps.order.models.enums.order_status import OrderStatus
from apps.order.services.coupon_helper import CouponHelper
from apps.payment.models.enums import PaymentType

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
    def get_total_cart(self) -> Decimal:
        total = sum(
            [i.get_total_item_price for i in self.products_cart.all()]
        ) if self.products_cart.all() else Decimal("0")
        return total

    @property
    def get_promo_code_sale(self) -> int:
        if self.promo_code and self.customer:
            helper = CouponHelper(self.promo_code, self, self.customer)
            return helper.final_sale()[0]
        return 0

    @property
    def get_final_sale(self) -> int:
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

        total = sale + self.delivery.delivery_sale if self.delivery else sale
        return total

    @property
    def get_total_with_sale(self) -> Decimal:
        """ общая скидка с промокодом и бонусами если есть """
        # todo: по сути бессмыслица, удалить это поле и там где оно использется написать total - final_price
        total = self.get_total_cart - self.get_final_sale
        return total

    def _get_active_bonus_rule(self) -> Optional[Bonus]:
        bonus_rule = Bonus.objects.filter(
            institutions=self.institution, is_active=True
        ).first()
        return bonus_rule

    @property
    def get_bonus_accrual(self) -> int:
        """ Max accrual amount """
        bonus_rule = self._get_active_bonus_rule()
        total = 0
        if bonus_rule:
            if self.promo_code:
                total = round((bonus_rule.accrual / Decimal('100')) * (self.get_total_cart - self.get_promo_code_sale))
            else:
                total = round((bonus_rule.accrual / Decimal('100')) * self.get_total_cart)
        return total

    @property
    def get_bonus_write_off(self) -> int:
        """ Max write off amount """
        bonus_rule = self._get_active_bonus_rule()
        total = 0
        if bonus_rule:
            if self.promo_code:
                total = round((bonus_rule.write_off / Decimal('100')) * (self.get_total_cart - self.get_promo_code_sale))
            else:
                total = round((bonus_rule.write_off / Decimal('100')) * self.get_total_cart)
        return total

    @property
    def final_price(self) -> float:
        """ """
        # TODO: CHECK THAT SALE NOT MORE THAN PRICE AMOUNT AFTER ALL (LIMIT BONUS WRITE OFF RULE?!)
        delivery_price = self.delivery.final_delivery_price if self.delivery else 0
        total = self.get_total_with_sale + delivery_price
        return Decimal("1") if total == 0 else total  # fixme: typing

    @property
    def get_min_order_amount_for_checkout(self):
        """
        вывести все условия мин суммы заказа для чекаута из самого заказа или из доставки
        """
        pass

    def __str__(self):
        return f'{self.id}: {self.institution}, {self.customer}, ' \
               f'{self.get_total_cart}'
