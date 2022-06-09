from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.order.models import Bonus
from apps.company.models import MinCartCost

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
    customer = models.OneToOneField(User,
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
        total = 0
        for i in self.items.all():
            total += i.get_total_item_price
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

        # TODO: подумать куда лучше (здесь или в get_total_cart)
        if self.customer_bonus is not None:
            bonus = Bonus.objects.get(institution=self.institution)
            if bonus.is_active and bonus.is_promo_code is False:
                return total - self.customer_bonus

        if self.delivery is not None:
            delivery_price = self.delivery.type.delivery_price
            free_delivery_amount = self.delivery.type.free_delivery_amount
            if delivery_price:
                if free_delivery_amount:
                    if total > free_delivery_amount:
                        total = total
                    else:
                        total += delivery_price
                else:
                    total += delivery_price

            delivery_sale = self.delivery.type.sale_amount
            if delivery_sale:
                if self.delivery.type.sale_type == "absolute":
                    total -= delivery_sale
                if self.delivery.type.sale_type == "percent":
                    total -= round((delivery_sale / Decimal('100')) * total)

        return total

    def __str__(self):
        return f'Cart {self.id}: {self.institution} -> {self.customer}, {self.get_total_cart}'
