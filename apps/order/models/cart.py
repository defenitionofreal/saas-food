from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.order.models import Bonus
from apps.delivery.models.enums import DeliveryType, SaleType

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
import json

User = get_user_model()


def calc_rounded_price(a, b):
    return round((a / Decimal('100')) * b)


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.ForeignKey("order.PromoCode",
                                   on_delete=models.SET_NULL,
                                   related_name="cart_promo_code",
                                   null=True,
                                   blank=True)
    customer_bonus = models.PositiveIntegerField(blank=True,
                                                 null=True)
    delivery = models.ForeignKey("delivery.DeliveryInfo",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="cart_delivery")
    min_amount = models.PositiveIntegerField(blank=True,
                                             null=True)
    items = models.ManyToManyField("order.CartItem",
                                   related_name="cart_items")
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  unique=True)

    @property
    def get_total_cart(self):
        q = self.items.all()
        return sum([i.get_total_item_price for i in q])

    @property
    def get_delivery_price(self):
        if self.delivery is not None:
            if self.delivery.type:
                return self.delivery.type.delivery_price

    @property
    def get_free_delivery_amount(self):
        if self.delivery is not None:
            if self.delivery.type.free_delivery_amount:
                return self.delivery.type.free_delivery_amount

    @property
    def get_delivery_sale_discount(self):
        """returns negative value to decrease the price"""
        if not self.delivery:
            return 0

        delivery_sale = -1.0 * self.delivery.type.sale_amount

        is_absolute_sale = delivery_sale and self.delivery.type.sale_type == SaleType.ABSOLUTE
        is_percent_sale = delivery_sale and self.delivery.type.sale_type == SaleType.PERCENT

        if is_absolute_sale:
            return delivery_sale

        if is_percent_sale:
            total = self.get_total_cart_consider_sale
            return calc_rounded_price(delivery_sale, total)

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
    def is_promo_code_absolute_sale(self):
        return self.promo_code and self.promo_code.code_type == SaleType.ABSOLUTE

    @property
    def is_promo_code_percent_sale(self):
        return self.promo_code and self.promo_code.code_type == SaleType.PERCENT

    @property
    def get_sale(self):
        if self.promo_code:
            sale = self.promo_code.sale

            items_cat = self.items.values("product__category",
                                          "product__slug",
                                          "product__price",
                                          "quantity")

            items_prod = self.items.values("product__slug",
                                           "product__price",
                                           "quantity")

            has_promo_code_categories = self.promo_code.categories.all()
            code_cat = []
            if has_promo_code_categories:
                code_cat = self.promo_code.categories.values_list("slug",
                                                                  flat=True)

            has_promo_code_products = self.promo_code.products.all()
            code_product = []
            if has_promo_code_products:
                code_product = self.promo_code.products.values_list("slug",
                                                                    flat=True)

            # ABSOLUTE SALE
            if self.is_promo_code_absolute_sale:
                # categories participate coupon
                if has_promo_code_categories:
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale
                # products participate coupon
                if has_promo_code_products:
                    for i in items_prod:
                        if i["product__slug"] in code_product:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale

                sale = sale if sale >= 0.0 else 0.0
                return sale

            # PERCENT SALE
            if self.is_promo_code_percent_sale:
                # categories participate coupon
                if has_promo_code_categories:
                    cat_total = 0
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            cat_total += i["product__price"] * i["quantity"]
                    cat_total = cat_total if cat_total >= 0.0 else 0.0
                    return calc_rounded_price(sale, cat_total)

                # products participate coupon
                if has_promo_code_products:
                    products_total = 0
                    for i in items_prod:
                        if i["product__slug"] in code_product:
                            products_total += i["product__price"] * i["quantity"]
                    products_total = products_total if products_total >= 0.0 else 0.0
                    return calc_rounded_price(sale, products_total)
                return calc_rounded_price(sale, self.get_total_cart)

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
    def get_total_cart_consider_sale(self):
        with_sale = self.get_total_cart_after_sale
        return with_sale if with_sale else self.get_total_cart

    @property
    def get_bonus_accrual(self):
        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active:
            sale_total = self.get_total_cart_after_sale if bonus.is_promo_code is True else self.get_total_cart
            return calc_rounded_price(bonus.accrual, sale_total)

    @property
    def has_free_delivery(self):
        return self.promo_code and self.promo_code.delivery_free is True

    @property
    def has_free_delivery_amount(self):
        if self.delivery:
            return bool(self.delivery.type.free_delivery_amount)

    def get_bonus_contrib_discount_to_final_price(self):
        """returns negative value to sum up with total (bonus should decrease the price)"""
        if not self.customer_bonus:
            return 0

        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active and bonus.is_promo_code is False:
            return -1.0 * self.customer_bonus

    def get_delivery_cost_for_delivery_zone(self, total):
        if self.get_delivery_zone["free_delivery_amount"]:
            if total < self.get_delivery_zone["free_delivery_amount"]:
                return self.get_delivery_zone["price"]
        return self.get_delivery_zone["price"]

    def get_delivery_cost_for_free_delivery_amount(self, total):
        assert self.has_free_delivery_amount
        free_delivery_amount = self.delivery.type.free_delivery_amount
        if free_delivery_amount:
            if total < free_delivery_amount:
                return total
        else:
            return self.get_delivery_price

    def get_delivery_cost_contribution_to_final_price(self, total):
        if not self.delivery or self.has_free_delivery:
            return 0

        # check for courier type and delivery zone
        if self.get_delivery_zone:
            total += self.get_delivery_cost_for_delivery_zone(total)
        else:
            if self.has_free_delivery_amount:
                total += self.get_delivery_cost_for_free_delivery_amount(total)

        total += self.get_delivery_sale_discount

    @property
    def final_price(self):
        total = self.get_total_cart_consider_sale

        bonus_contrib = self.get_bonus_contrib_discount_to_final_price()
        total += bonus_contrib

        # this was in the original code
        # if bonus_contrib == 0:
        #     return total

        delivery_contrib = self.get_delivery_cost_contribution_to_final_price(total)
        total += delivery_contrib
        return total

    def __str__(self):
        return f'Cart {self.id}: {self.institution} -> {self.customer}, {self.get_total_cart}'
