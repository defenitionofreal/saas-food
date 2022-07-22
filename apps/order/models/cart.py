from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

from django.db.models import F

from apps.order.models import Bonus
from apps.delivery.models.enums import DeliveryType

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
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

    # +
    @property
    def get_total_cart(self):
        total = 0
        for i in self.items.all():
            total += i.get_total_item_price
        return total

    # +
    @property
    def get_delivery_price(self):
        if self.delivery is not None:
            if self.delivery.type.delivery_price:
                return self.delivery.type.delivery_price

    # +
    @property
    def get_free_delivery_amount(self):
        if self.delivery is not None:
            if self.delivery.type.free_delivery_amount:
                return self.delivery.type.free_delivery_amount

    # +
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

    # +
    @property
    def get_min_delivery_order_amount(self):
        if self.delivery is not None:
            return self.delivery.type.min_order_amount

    # +
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

    # +
    @property
    def get_sale(self):
        if self.promo_code:
            sale = self.promo_code.sale
            # if absolute sale type
            if self.promo_code.code_type == 'absolute':
                # categories participate coupon
                if self.promo_code.categories.all():
                    items_cat = self.items.values("product__category",
                                                  "product__slug",
                                                  "product__price",
                                                  "quantity")
                    code_cat = self.promo_code.categories.values_list("slug",
                                                                      flat=True)
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale
                # products participate coupon
                if self.promo_code.products.all():
                    items = self.items.values("product__slug",
                                              "product__price",
                                              "quantity")
                    code_product = self.promo_code.products.values_list("slug",
                                                                        flat=True)
                    for i in items:
                        if i["product__slug"] in code_product:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale

                sale = sale if sale >= 0.0 else 0.0
                return sale

            # if percent sale type
            if self.promo_code.code_type == 'percent':

                # categories participate coupon
                if self.promo_code.categories.all():
                    cat_total = 0
                    items_cat = self.items.values("product__category",
                                                  "product__slug",
                                                  "product__price",
                                                  "quantity")
                    code_cat = self.promo_code.categories.values_list("slug",
                                                                      flat=True)
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            cat_total += i["product__price"] * i["quantity"]
                    cat_total = cat_total if cat_total >= 0.0 else 0.0
                    return round((sale / Decimal('100')) * cat_total)

                # products participate coupon
                if self.promo_code.products.all():
                    products_total = 0
                    items = self.items.values("product__slug",
                                              "product__price",
                                              "quantity")
                    code_product = self.promo_code.products.values_list("slug",
                                                                        flat=True)
                    for i in items:
                        if i["product__slug"] in code_product:
                            products_total += i["product__price"] * i[
                                "quantity"]
                    products_total = products_total if products_total >= 0.0 else 0.0
                    return round((sale / Decimal('100')) * products_total)

                return round((sale / Decimal('100')) * self.get_total_cart)
        return None

    # +
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

    # +
    @property
    def get_bonus_accrual(self):
        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active:
            if bonus.is_promo_code is True:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart_after_sale)
            else:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart)
            return total_accrual

    # +
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
        return f'Cart {self.id}: {self.institution} -> {self.customer}, {self.get_total_cart}'

    def __iadd__(self, other):
        if not isinstance(other, Cart):
            return
        other_items = other.items.all()
        for i in other_items:
            product_dict = i.product
            quantity = i.quantity
            self.add_item(product_dict, quantity)
        return self

    def add_item(self, product_dict: dict, quantity=1):
        """ add new item to cart or update quantity of an item """
        from apps.order.models import CartItem
        cart_item, cart_item_created = CartItem.objects.get_or_create(product=product_dict,
                                                                      cart=self)

        if self.items.filter(product=product_dict).exists():
            cart_item.quantity = F("quantity") + quantity
            cart_item.save(update_fields=("quantity",))
        else:
            self.items.add(cart_item)
