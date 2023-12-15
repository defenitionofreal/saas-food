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

User = get_user_model()


class Cart(models.Model):
    """
    A model that contains data for a shopping cart.
    Minimum amount at cart (if added)
    delivery cost (if added) ?! or in order model?
    promo code (coupon) for sale
    add bonus points to a customer profile or he could spend his points
    """
    _promo_code_sale = 0

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
    def get_final_delivery_price(self) -> Decimal:
        return self.delivery.final_delivery_price if self.delivery else Decimal("0")

    @property
    def get_free_delivery_amount(self) -> Decimal:
        return self.delivery.free_delivery_amount if self.delivery else Decimal("0")

    @property
    def get_min_delivery_order_amount(self) -> int:
        return self.delivery.min_delivery_order_amount if self.delivery else 0

    @property
    def get_total_cart(self) -> Decimal:
        total = sum([i.get_total_item_price for i in self.products_cart.all()]
                    ) if self.products_cart.all() else Decimal("0")
        return total

    @property
    def get_promo_code_sale(self) -> Decimal:
        if self.promo_code and not self._promo_code_sale:
            self._promo_code_sale = CouponHelper(self.promo_code, self).final_sale
        return Decimal(self._promo_code_sale)

    @property
    def get_final_sale(self) -> int:
        """
        Sale includes coupon, bonus amount and delivery sale
        """
        return sum([self.get_promo_code_sale, self.customer_bonus])

    def _get_active_bonus_rule(self) -> Optional[Bonus]:
        bonus_rule = Bonus.objects.filter(
            institutions=self.institution, is_active=True
        ).first()
        return bonus_rule

    @property
    def get_bonus_accrual(self) -> int:
        """ Max accrual amount """
        # todo: не учитывается стоимость доставки, нужно ли?
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
        # todo: не учитывается стоимость доставки, нужно ли?
        bonus_rule = self._get_active_bonus_rule()
        total = 0
        if bonus_rule:
            if self.promo_code:
                total = round((bonus_rule.write_off / Decimal('100')) * (self.get_total_cart - self.get_promo_code_sale))
            else:
                total = round((bonus_rule.write_off / Decimal('100')) * self.get_total_cart)
        return total

    @property
    def final_price(self) -> Decimal:
        total = self.get_total_cart - self.get_final_sale + self.get_final_delivery_price
        return max(total, Decimal("1"))

    @property
    def min_amount_for_checkout(self):
        """
        Условия мин суммы заказа для чекаута из заказа или из доставки/зоны
        """
        cart_cost = self.institution.min_cart_cost.first().cost if self.institution.min_cart_cost.exists() else 0
        delivery_cost = self.get_min_delivery_order_amount
        return delivery_cost if delivery_cost > cart_cost else cart_cost

    def __str__(self):
        return f'{self.id}: {self.institution}, {self.customer}, ' \
               f'{self.get_total_cart}'
