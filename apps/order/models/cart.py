from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from apps.order.models import Bonus
from apps.order.models.enums.order_status import OrderStatus

from apps.delivery.models.enums import DeliveryType
from apps.payment.models.enums import PaymentType

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
from decimal import Decimal

from itertools import product as pr
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
    customer_bonus = models.PositiveIntegerField(blank=True,
                                                 null=True)
    # order min amount rule
    min_amount = models.PositiveIntegerField(blank=True,
                                             null=True)

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
    items = models.ManyToManyField("order.CartItem",
                                   related_name="cart_items")
    code = models.CharField(max_length=5,
                            blank=True,
                            null=True)
    status = models.CharField(max_length=10,
                              choices=OrderStatus.choices,
                              default=OrderStatus.DRAFT)
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  unique=True)
    # paid field should be for an online payment only?
    paid = models.BooleanField(default=False)

    @property
    def get_total_cart(self):
        total = 0
        if self.items.all():
            total = sum([i.get_total_item_price for i in self.items.all()])
        return total

    @property
    def get_delivery_price(self):
        if self.delivery is not None:
            if self.delivery.type.delivery_price:
                return self.delivery.type.delivery_price

    @property
    def get_free_delivery_amount(self):
        if self.delivery is not None:
            if self.delivery.type.free_delivery_amount:
                return self.delivery.type.free_delivery_amount

    @property
    def get_delivery_sale(self):
        if self.delivery is not None:
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
        return None

    @property
    def get_min_delivery_order_amount(self):
        if self.delivery is not None:
            return self.delivery.type.min_order_amount

    @property
    def get_delivery_zone(self):
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
        return None

    @property
    def delivery_cost(self):
        cost = self.get_delivery_price
        if self.delivery.type.free_delivery_amount:
            if self.get_total_cart_after_sale > self.delivery.type.free_delivery_amount:
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
    def get_sale(self):
        if self.promo_code:
            sale = self.promo_code.sale
            count_sale = 0
            coupon_categories = self.promo_code.categories.all()
            coupon_products = self.promo_code.products.all()
            cart_items = self.items.values("product__category",
                                           "product__slug",
                                           "product__price",
                                           "quantity")
            # only categories products
            if coupon_categories and not coupon_products:
                for cat in coupon_categories:
                    products = cat.products.filter(is_active=True).only("slug")
                    for product, item in pr(products, cart_items):
                        if product.slug in item["product__slug"]:
                            count_sale += item["product__price"] * item["quantity"]

            # only still products
            if coupon_products and not coupon_categories:
                for product, item in pr(coupon_products, cart_items):
                    if product.slug in item["product__slug"]:
                        count_sale += item["product__price"] * item["quantity"]

            # categories and products together
            if coupon_products and coupon_categories:
                coupon_items = []
                for cat in coupon_categories:
                    products = cat.products.filter(is_active=True).only("slug")
                    for product in products:
                        coupon_items.append(product.slug)
                for product in coupon_products:
                    coupon_items.append(product.slug)
                for item in cart_items:
                    if item["product__slug"] in coupon_items:
                        count_sale += item["product__price"] * item["quantity"]

            # no cats and no products, so look to the cart total
            if not coupon_products and not coupon_categories:
                count_sale = self.get_total_cart

            if self.promo_code.code_type == 'absolute':
                final_sale = sale if sale >= 0.0 else 0.0
                return final_sale

            if self.promo_code.code_type == 'percent':
                final_sale = round((sale / Decimal('100')) * count_sale)
                return final_sale

            # TODO:  НУЖНО ПЕРЕПИСАТЬ ЛОГИКУ ПРОМОКОДОВ НА:
            #  + если не выбраны товары или категории, то купон действует на всю корзину
            #  + если выбраны то купон действует только на выбранные товары и считает скидку после суммы этих товаров в корзине
            #  - проблема с счетом если есть модификаторы и добавки, считает стандартную цену!
            #  - в абсолютной скидке , отнимать значение от каждой позиции, если не выбран товар или категория то отнимат от общей суммы корзины !
        return None

    @property
    def get_total_cart_after_sale(self):
        total = self.get_total_cart
        sale = 0
        if self.get_sale is not None:
            sale = self.get_sale
        if self.customer_bonus is not None:
            bonus = Bonus.objects.get(institution=self.institution)
            if bonus.is_active and bonus.is_promo_code is True:
                return total - (sale + self.customer_bonus)
        return total - sale

    @property
    def get_bonus_accrual(self):
        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active:
            if bonus.is_promo_code is True:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart_after_sale)
            else:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart)
            return total_accrual

    @property
    def final_price(self):
        total = self.get_total_cart
        with_sale = self.get_total_cart_after_sale
        if with_sale:
            total = with_sale

        # minus bonus points from total
        if self.customer_bonus is not None:
            bonus = Bonus.objects.get(institution=self.institution)
            if bonus.is_active and bonus.is_promo_code is False:
                return total - self.customer_bonus

        if self.delivery is not None:
            delivery_price = self.delivery.type.delivery_price
            free_delivery_amount = self.delivery.type.free_delivery_amount

            if self.promo_code and self.promo_code.delivery_free is True:
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

        return total

    def __str__(self):
        return f'{self.id}: {self.institution}, {self.customer}, {self.get_total_cart}'

    def save(self, *args, **kwargs):
        if not self.code:
            from apps.order.services.generate_order_number import \
                _generate_order_number
            self.code = _generate_order_number(1, 3)
        super().save(*args, **kwargs)
