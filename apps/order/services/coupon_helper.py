from rest_framework.exceptions import ValidationError

from apps.order.models import PromoCodeUser
from apps.delivery.models.enums import SaleType
from decimal import Decimal

import datetime
import itertools


class CouponHelper:
    """
    Main coupon class with all needed funcs and counts
    """

    def __init__(self, coupon, cart, user):
        self.coupon = coupon
        self.cart = cart
        self.user = user

    def final_sale(self) -> tuple:
        final_sale = 0
        amount_for_sale = 0
        coupon_sale = self.coupon.sale
        coupon_categories = self.coupon.categories.all()
        coupon_products = self.coupon.products.all()
        cart_items = self.cart.products_cart.only("item", "quantity", "modifier", "additives")

        print("CART ITEMS QS", cart_items) # fixme: repeats 5 times!

        # only categories products
        if coupon_categories and not coupon_products:
            for cat in coupon_categories:
                products = cat.products.filter(is_active=True).only("id")
                for product, cart_item in itertools.product(products, cart_items):
                    if product.id == cart_item.item.id:
                        amount_for_sale += cart_item.get_total_item_price

        # only still products
        if coupon_products and not coupon_categories:
            for product, cart_item in itertools.product(coupon_products, cart_items):
                if product.id == cart_item.item.id:
                    amount_for_sale += cart_item.get_total_item_price

        # categories and products together
        if coupon_products and coupon_categories:
            coupon_items = [product.id
                            for cat in coupon_categories
                            for product in cat.products.filter(is_active=True).only("id")]
            coupon_items += [product.id for product in coupon_products]
            coupon_items = list(set(coupon_items))
            matching_items = cart_items.filter(item_id__in=coupon_items)
            for cart_item in matching_items:
                amount_for_sale += cart_item.get_total_item_price

        # no cats and no products, so look to the cart total
        if not coupon_products and not coupon_categories:
            amount_for_sale = self.cart.get_total_cart

        if self.coupon.code_type == 'absolute':
            final_sale = coupon_sale if coupon_sale >= 0.0 else 0.0
            return final_sale, amount_for_sale

        if self.coupon.code_type == 'percent':
            final_sale = round((coupon_sale / Decimal('100')) * amount_for_sale)
            return final_sale, amount_for_sale

        return final_sale, amount_for_sale

    # RULES
    def validate_coupon_with_bonus(self):
        bonus = self.cart.institution.bonuses.filter(is_active=True).first()
        if self.cart.customer_bonus > 0 and bonus and not bonus.is_promo_code:
            raise ValidationError(
                {"detail": "Use promo code with bonuses is not allowed."})

    def validate_sale(self):
        """ Not allowing to write off more than a final price """
        code_type = self.coupon.code_type
        if code_type == SaleType.ABSOLUTE and (self.final_sale()[1] - self.coupon.sale) <= 0:
            raise ValidationError({"detail": f"Sale {self.final_sale()[0]} is bigger than {self.final_sale()[1]}"})
        if code_type == SaleType.PERCENT and self.coupon.sale > 100:
            raise ValidationError({"detail": "Sale is bigger 100%"})

    def validate_total_cart(self):
        """
        Not allowing to use coupon if min coupon cart price > actual cart total
        """
        if self.coupon.cart_total > 0 and self.cart.get_total_cart < self.coupon.cart_total:
            raise ValidationError(
                {"detail": f"Cart price has to be more {self.coupon.cart_total}"})

    def validate_dates(self):
        """
        Not allowing to use coupon sooner or later from actual dates
        """
        now_date = datetime.datetime.now().date()
        if self.coupon.date_start and now_date < self.coupon.date_start:
            raise ValidationError({"detail": f"Code period is not started yet."})
        if self.coupon.date_finish and now_date >= self.coupon.date_finish:
            raise ValidationError({"detail": f"Code period is expired."})

    def validate_tied_categories(self):
        if self.coupon.categories.all() and not self.coupon.products.all():
            cart_item_categories = set(self.cart.products_cart.values_list("item__category_id", flat=True))
            coupon_categories = set(self.coupon.categories.values_list("promocode__categories__id", flat=True))
            if not cart_item_categories.intersection(coupon_categories):
                raise ValidationError({"detail": "Cart product categories are not tied with coupon."})

    def validate_tied_products(self):
        if self.coupon.products.all() and not self.coupon.categories.all():
            cart_items = set(self.cart.products_cart.values_list("item__id", flat=True))
            coupon_items = set(self.coupon.products.values_list("promocode__products__id", flat=True))
            if not cart_items.intersection(coupon_items):
                raise ValidationError({"detail": "Cart items are not tied with coupon."})

    def validate_tied_products_and_categories_together(self):
        if self.coupon.products.all() and self.coupon.categories.all():
            coupon_items = []
            coupon_categories = self.coupon.categories.all()
            coupon_products = self.coupon.products.values_list("id", flat=True)
            cart_items = self.cart.products_cart.values_list("item__id", flat=True)
            for category in coupon_categories:
                for product in category.products.values_list("id", flat=True):
                    coupon_items.append(product)
            for p in coupon_products:
                coupon_items.append(p)

            is_included = any(item in coupon_items for item in cart_items)

            if not is_included:
                raise ValidationError({"detail": "Cart items are not tied with coupon."})

    def validate_num_uses(self):
        if self.coupon.code_use > 0 and self.coupon.num_uses >= self.coupon.code_use:
            raise ValidationError({"detail": "Max level exceeded for coupon."})

    def validate_user_num_uses(self) -> PromoCodeUser:
        coupon_per_user, _ = PromoCodeUser.objects.get_or_create(
            code=self.coupon, user=self.user
        )
        if self.coupon.code_use_by_user > 0 and coupon_per_user.num_uses >= self.coupon.code_use_by_user:
            raise ValidationError({"detail": "User's max level exceeded for coupon."})
        return coupon_per_user

    def main(self):

        if self.cart.promo_code:
            raise ValidationError({"detail": "Promo code already applied."})

        if not self.coupon.is_active:
            raise ValidationError({"detail": "Code is not active."})

        self.validate_coupon_with_bonus()
        self.validate_sale()
        self.validate_total_cart()
        self.validate_dates()
        self.validate_tied_categories()
        self.validate_tied_products()
        self.validate_tied_products_and_categories_together()
        self.validate_num_uses()

        user_num_uses_rule = self.validate_user_num_uses()
        if isinstance(user_num_uses_rule, PromoCodeUser):
            user_num_uses_rule.num_uses += 1
            user_num_uses_rule.save()

        self.coupon.num_uses += 1
        self.coupon.save()
        self.cart.promo_code = self.coupon
        self.cart.save()
