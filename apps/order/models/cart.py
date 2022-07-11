from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework.generics import get_object_or_404
from django.db.models import F

from apps.delivery.models import Delivery
from apps.order.models import Bonus
from apps.delivery.models.enums import DeliveryType, SaleType
from .cart_item import CartItem

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
import json

from apps.product.models import Product
from ..services.math_utils import get_absolute_from_percent_and_total

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

    def __str__(self):
        return f'Cart {self.id}: {self.institution} -> {self.customer}, {self.get_total_cart}'

    @property
    def get_total_cart(self):
        q = self.items.all()
        s = sum([i.get_total_item_price for i in q])
        return Decimal(s)

    @property
    def has_not_promo_code_bonus(self):
        if self.customer_bonus is not None:
            bonus = Bonus.objects.filter(institution=self.institution).first()
            return bonus and bonus.is_promo_code is False
        return False

    # ======== DELIVERY ========

    def get_delivery_model(self) -> Delivery:
        if self.delivery:
            return self.delivery.type

    @property
    def get_delivery_sale(self):
        dm = self.get_delivery_model()
        if dm:
            return dm.get_delivery_sale_amount()
        return 0

    @property
    def get_delivery_price(self):
        if self.delivery is not None:
            if self.delivery.type:
                return self.delivery.type.delivery_price

    @property
    def has_free_delivery_amount(self):
        dm = self.get_delivery_model()
        if dm:
            return dm.has_free_delivery_amount
        return False

    @property
    def get_free_delivery_amount(self):
        if self.has_free_delivery_amount:
            return self.delivery.type.free_delivery_amount

    @property
    def has_free_delivery(self):
        """whether delivery is free in any case"""
        return self.promo_code and self.promo_code.delivery_free is True

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
                    # todo: replace literal keys with variables
                    return {"title": zone.title,
                            "price": zone.price,
                            "free_delivery_amount": zone.free_delivery_amount,
                            "min_order_amount": zone.min_order_amount,
                            "delivery_time": zone.delivery_time}
        return None

    def get_delivery_cost_for_delivery_zone(self, total):
        if self.get_delivery_zone["free_delivery_amount"]:
            if total < self.get_delivery_zone["free_delivery_amount"]:
                return self.get_delivery_zone["price"]
        return self.get_delivery_zone["price"]

    def get_final_delivery_cost(self, total):
        if not self.delivery or self.has_free_delivery:
            return 0

        dm = self.get_delivery_model()
        if not dm:
            return 0

        cost = 0

        if self.get_delivery_zone:
            cost += self.get_delivery_cost_for_delivery_zone(total)
        else:
            cost += dm.get_delivery_cost(total)

        discount = dm.get_delivery_discount(total)
        return cost - discount

    # ======== PROMO CODE ========

    def get_promo_code_type(self):
        if self.promo_code:
            return self.promo_code.code_type

    @property
    def is_promo_code_absolute_sale(self):
        return self.get_promo_code_type() == SaleType.ABSOLUTE

    @property
    def is_promo_code_percent_sale(self):
        return self.get_promo_code_type() == SaleType.PERCENT

    @property
    def get_bonus_accrual(self):
        """ amount of bonus money given to customer after this order """
        bonus = Bonus.objects.get(institution=self.institution)
        if bonus and bonus.is_active:
            if bonus.is_promo_code is True:
                sale_total = self.get_total_cart_after_sale
            else:
                sale_total = self.get_total_cart
            return get_absolute_from_percent_and_total(bonus.accrual, sale_total)
        return 0

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
                    return get_absolute_from_percent_and_total(sale, cat_total)

                # products participate coupon
                if has_promo_code_products:
                    products_total = 0
                    for i in items_prod:
                        if i["product__slug"] in code_product:
                            products_total += i["product__price"] * i["quantity"]
                    products_total = products_total if products_total >= 0.0 else 0.0
                    return get_absolute_from_percent_and_total(sale, products_total)
                return get_absolute_from_percent_and_total(sale, self.get_total_cart)

        return 0

    def get_promo_code_bonus_contrib_to_total(self):
        """
        discount from bonus promo code
        :return: value <= 0
        """
        if self.customer_bonus is not None:
            bonus = Bonus.objects.get(institution=self.institution)
            if bonus.is_active and bonus.is_promo_code is True:
                return -1 * self.customer_bonus
        return 0

    def get_sale_contrib_to_total(self):
        return -1 * Decimal(self.get_sale)

    @property
    def get_total_cart_after_sale(self):
        """ order cost after discounts applied"""
        total = self.get_total_cart
        sale_contrib = self.get_sale_contrib_to_total()
        promo_code_bonus_contrib = self.get_promo_code_bonus_contrib_to_total()
        return total + sale_contrib + promo_code_bonus_contrib

    def get_customer_bonus_contrib_to_final_price(self):
        """
        discount amount
        :return: value <= 0
        """
        if not self.customer_bonus:
            return 0

        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active and bonus.is_promo_code is False:
            return -1 * self.customer_bonus

        return 0

    @property
    def final_price(self):
        """ final money amount for customer to pay """
        total = self.get_total_cart_after_sale

        bonus_contrib = self.get_customer_bonus_contrib_to_final_price()
        delivery_contrib = self.get_final_delivery_cost(total)

        total += bonus_contrib + delivery_contrib
        return total

    # ========================================
    def add_product_to_cart(self, product_dict):
        cart_item, cart_item_created = CartItem.objects.get_or_create(product=product_dict, cart=self)
        do_update_quantity = not cart_item_created

        if do_update_quantity:
            cart_item.quantity = F("quantity") + 1
            cart_item.save(update_fields=("quantity",))
        else:
            self.items.add(cart_item)

    def remove_product_by_slug(self, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        has_product_items = self.items.filter(product__slug=product.slug).exists()
        if not has_product_items:
            return

        cart_item = self.items.get(product__slug=product.slug, cart=self)
        if cart_item.quantity > 1:
            cart_item.quantity = F("quantity") - 1
            cart_item.save(update_fields=("quantity",))
        else:
            self.items.remove(cart_item)
