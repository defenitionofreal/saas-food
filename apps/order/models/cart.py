from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.order.models import Bonus

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
    customer = models.OneToOneField(User, on_delete=models.CASCADE,
                                    related_name='cart_customer',
                                    null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.ForeignKey("order.PromoCode", on_delete=models.SET_NULL,
                                   related_name="cart_promo_code", null=True,
                                   blank=True)
    customer_bonus = models.ForeignKey("order.Bonus", on_delete=models.SET_NULL,
                                       blank=True, null=True,
                                       related_name="cart_bonus")
    #delivery_cost = models.
    min_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    items = models.ManyToManyField("order.CartItem", related_name="cart_items")

    @property
    def get_total_cart(self):
        total = 0
        for i in self.items.all():
            total += i.get_single_item_total
        return total

    @property
    def get_sale(self):
        sale = self.promo_code.sale

        if self.promo_code.code_type == 'absolute':

            # if self.promo_code.categories.all():
            #     cat_total = 0
            #     for i in self.items.all():
            #         if i.product.category in self.promo_code.categories.all():
            #             print(i)
            #             cat_total += i.product.price * i.quantity
            #     print(cat_total)
            #     print(sale)
            #     return cat_total
            #
            # if self.promo_code.products.all():
            #     products_total = 0
            #     for i in self.items.all():
            #         if i.product in self.promo_code.products.all():
            #             products_total += i.product.price * i.quantity
            #     return products_total - sale
            sale = sale if sale >= 0.0 else 0.0
            return sale

        if self.promo_code.code_type == 'percent':

            if self.promo_code.categories.all():
                cat_total = 0
                for i in self.items.all():
                    if i.product.category in self.promo_code.categories.all():
                        cat_total += i.product.price * i.quantity
                return round((sale / Decimal('100')) * cat_total)

            if self.promo_code.products.all():
                products_total = 0
                for i in self.items.all():
                    if i.product in self.promo_code.products.all():
                        products_total += i.product.price * i.quantity
                return round((sale / Decimal('100')) * products_total)

            return round((sale / Decimal('100')) * self.get_total_cart)

    @property
    def get_total_cart_after_sale(self):
        total = self.get_total_cart
        sale = self.get_sale
        # if self.promo_code.code_type == 'absolute':
        #     return sale
        return total - sale

    @property
    def get_bonus_accrual(self):
        bonus = Bonus.objects.get(institution=self.institution)
        if bonus.is_active:
            if bonus.is_promo_code:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart_after_sale)
            else:
                total_accrual = round((bonus.accrual / Decimal('100')) * self.get_total_cart)
            return total_accrual

    def __str__(self):
        return f'Cart: {self.institution} -> {self.customer}, {self.get_total_cart}'
