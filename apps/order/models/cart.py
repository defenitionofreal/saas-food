from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

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
    # dates part
    delivery_date = models.DateField(blank=True,
                                     null=True)
    time_from = models.DateTimeField(blank=True,
                                     null=True)
    time_till = models.DateTimeField(blank=True,
                                     null=True)
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
    delivery = models.ForeignKey("delivery.DeliveryInfo",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="cart_delivery")
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
    def get_total_cart(self) -> int:
        total = sum(
            [i.get_total_item_price for i in self.products_cart.all()]
        ) if self.products_cart.all() else 0
        return total

    @property
    def get_delivery_price(self) -> int:
        price = 0
        if self.delivery and self.delivery.type.delivery_price:
            price = self.delivery.type.delivery_price
        return price

    @property
    def get_free_delivery_amount(self) -> int:
        amount = 0
        if self.delivery and self.delivery.type.free_delivery_amount:
            amount = self.delivery.type.free_delivery_amount
        return amount

    @property
    def get_delivery_sale(self) -> int:
        if self.delivery:
            delivery_sale = self.delivery.type.sale_amount
            total = self.get_total_cart
            with_sale = self.get_total_cart_after_sale
            if with_sale:
                total = with_sale
            if delivery_sale:
                if self.delivery.type.sale_type == "absolute":
                    return delivery_sale
                if self.delivery.type.sale_type == "percent":
                    return round((delivery_sale / Decimal('100')) * total)
        return 0

    @property
    def get_min_delivery_order_amount(self) -> int:
        amount = 0
        if self.delivery:
            amount = self.delivery.type.min_order_amount
        return amount

    @property
    def get_delivery_zone(self) -> dict:
        zones = self.institution.dz.filter(is_active=True)
        if zones.exists() and self.delivery.type.delivery_type == DeliveryType.COURIER:
            for zone in zones:
                address = self.delivery.address.address
                point = Point([json.loads(address.latitude),
                               json.loads(address.longitude)])
                polygon = Polygon(json.loads(
                    zone.dz_coordinates.values_list("coordinates",
                                                    flat=True)[0]))
                if boolean_point_in_polygon(point, polygon):
                    return {"title": zone.title,
                            "price": zone.price,
                            "free_delivery_amount": zone.free_delivery_amount,
                            "min_order_amount": zone.min_order_amount,
                            "delivery_time": zone.delivery_time}
        return {}

    @property
    def delivery_cost(self) -> int:
        cost = self.get_delivery_price
        if self.delivery.type.free_delivery_amount and self.get_total_cart_after_sale > self.delivery.type.free_delivery_amount:
            cost = 0

        if self.get_delivery_zone:
            cost = self.get_delivery_zone["price"]
            if self.get_delivery_zone["free_delivery_amount"]:
                if self.get_total_cart_after_sale > self.get_delivery_zone["free_delivery_amount"]:
                    cost = 0

        if self.promo_code and self.promo_code.delivery_free is True:
            cost = 0

        return cost

    @property
    def get_promo_code_sale(self) -> int:
        if self.promo_code and self.customer:
            helper = CouponHelper(self.promo_code, self, self.customer)
            return helper.final_sale()[0]
        return 0

    @property
    def get_final_sale(self) -> int:
        return self.get_promo_code_sale + self.customer_bonus

    @property
    def get_total_cart_after_sale(self) -> float:
        # общая скидка с промокодом и бонусами если есть!
        # todo: по сути бессмыслица, удалить это поле и там где оно использется написать total - final_price
        total = self.get_total_cart
        sale = 0
        if self.get_promo_code_sale:
            sale = self.get_promo_code_sale
        if self.customer_bonus > 0:
            bonus = Bonus.objects.filter(
                institutions=self.institution,
                is_active=True,
                is_promo_code=True
            ).first()
            return total - (sale + self.customer_bonus) if bonus else total - sale
        return total - sale

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
        total = self.get_total_cart_after_sale

        # minus bonus points from total
        if self.customer_bonus > 0:
            bonus = Bonus.objects.get(institutions=self.institution)
            if bonus.is_active and not bonus.is_promo_code:
                return total - self.customer_bonus

        if self.delivery:
            delivery_price = self.delivery.type.delivery_price
            free_delivery_amount = self.delivery.type.free_delivery_amount

            if self.promo_code and self.promo_code.delivery_free:
                total = total
            else:
                # check for courier type and delivery zone
                if self.get_delivery_zone:
                    if self.get_delivery_zone["free_delivery_amount"]:
                        if total < self.get_delivery_zone["free_delivery_amount"]:
                            total += self.get_delivery_zone["price"]
                    else:
                        total += self.get_delivery_zone["price"]
                else:
                    if free_delivery_amount:
                        if total < free_delivery_amount:
                            total += total
                    else:
                        total += delivery_price

                # if delivery type has a sale
                delivery_sale = self.get_delivery_sale
                if delivery_sale:
                    total -= delivery_sale

        return Decimal("1") if total == 0 else total

    def __str__(self):
        return f'{self.id}: {self.institution}, {self.customer}, ' \
               f'{self.get_total_cart}'
