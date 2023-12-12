from rest_framework.exceptions import ValidationError

from apps.order.models import PromoCodeUser
from apps.delivery.models.enums import SaleType
from decimal import Decimal

import datetime


class CouponHelper:
    """
    Main coupon class with all needed funcs and counts
    """

    def __init__(self, coupon, cart):
        self.coupon = coupon
        self.cart = cart
        self.cart_items = self.cart.products_cart.select_related("item").only(
            "item", "quantity", "modifier", "additives"
        )
        self.coupon_categories = self.coupon.categories.all()
        self.coupon_products = self.coupon.products.all()
        self.amount_for_sale = self.cart_items_amount_for_coupon_sale()
        self.final_sale = self.cart_coupon_final_sale()

    def __coupon_categories_amount(self) -> Decimal:
        """
        If coupon has only some categories to apply
        """
        amount_for_sale = 0
        if self.coupon_categories and not self.coupon_products:
            product_ids = set(
                product.id for coupon_category in self.coupon_categories for product
                in coupon_category.products.filter(is_active=True).only("id"))
            amount_for_sale = sum(cart_item.get_total_item_price
                                  for cart_item in self.cart_items
                                  if cart_item.item.id in product_ids)
        return Decimal(amount_for_sale)

    def __coupon_products_amount(self) -> Decimal:
        """
        If coupon has only some products to apply
        """
        amount_for_sale = 0
        if self.coupon_products and not self.coupon_categories:
            product_ids = set(product.id for product in self.coupon_products)
            amount_for_sale += sum(cart_item.get_total_item_price
                                   for cart_item in self.cart_items
                                   if cart_item.item.id in product_ids)
        return Decimal(amount_for_sale)

    def __coupon_categories_and_products_amount(self) -> Decimal:
        """
        If coupon has only some categories and products to apply
        """
        amount_for_sale = 0
        if self.coupon_products and self.coupon_categories:
            coupon_item_ids = set(product.id for cat in self.coupon_categories
                                  for product in cat.products.filter(is_active=True).only("id"))
            coupon_item_ids.update(product.id for product in self.coupon_products)
            matching_items = self.cart_items.filter(item_id__in=coupon_item_ids)
            amount_for_sale += sum(cart_item.get_total_item_price
                                   for cart_item in matching_items)
        return Decimal(amount_for_sale)

    def __coupon_default_amount(self):
        """
        If coupon is for whole cart items
        """
        amount_for_sale = 0
        if not self.coupon_products and not self.coupon_categories:
            amount_for_sale = self.cart.get_total_cart - self.cart.customer_bonus
        return amount_for_sale

    def cart_items_amount_for_coupon_sale(self):
        """
        Count sum of all items to count sale from
        """
        amount_for_sale = 0
        amount_for_sale += self.__coupon_categories_amount()
        amount_for_sale += self.__coupon_products_amount()
        amount_for_sale += self.__coupon_categories_and_products_amount()
        amount_for_sale += self.__coupon_default_amount()
        return amount_for_sale

    def cart_coupon_final_sale(self):
        """
        Count final sale amount
        """
        coupon_sale = self.coupon.sale
        final_sale = 0
        if self.coupon.code_type == SaleType.ABSOLUTE:
            final_sale = coupon_sale if coupon_sale >= 0.0 else 0.0
        if self.coupon.code_type == SaleType.PERCENT:
            final_sale = round((coupon_sale / Decimal('100')) * self.amount_for_sale)
        return final_sale

    # RULES
    def validate_coupon_with_bonus(self):
        bonus_rule = self.cart.institution.bonuses.filter(
            is_active=True, is_promo_code=True
        ).first()
        if self.cart.customer_bonus > 0 and not bonus_rule:
            raise ValidationError(
                {"detail": "Use promo code with bonuses is not allowed."})

    def validate_sale(self):
        """ Not allowing to write off more than a final price """
        coupon_type = self.coupon.code_type
        if coupon_type == SaleType.ABSOLUTE and (self.amount_for_sale - self.coupon.sale) <= 0:
            raise ValidationError({"detail": f"Sale {self.final_sale} is bigger than {self.amount_for_sale}"})
        if coupon_type == SaleType.PERCENT and self.coupon.sale > 100:
            raise ValidationError({"detail": "Sale is bigger 100%"})

    def validate_final_cart_price(self):
        """
        Not allowing to use coupon if min coupon cart price > actual cart total
        """
        if self.coupon.cart_total > 0 and self.cart.final_price < self.coupon.cart_total:
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

    def validate_user_num_uses(self, user) -> PromoCodeUser:
        coupon_per_user, _ = PromoCodeUser.objects.get_or_create(
            code=self.coupon, user=user
        )
        if self.coupon.code_use_by_user > 0 and coupon_per_user.num_uses >= self.coupon.code_use_by_user:
            raise ValidationError({"detail": "User's max level exceeded for coupon."})
        return coupon_per_user

    def main(self, user):

        if self.cart.promo_code:
            raise ValidationError({"detail": "Promo code already applied."})

        if not self.coupon.is_active:
            raise ValidationError({"detail": "Code is not active."})

        self.validate_coupon_with_bonus()
        self.validate_sale()
        self.validate_final_cart_price()
        self.validate_dates()
        self.validate_tied_categories()
        self.validate_tied_products()
        self.validate_tied_products_and_categories_together()
        self.validate_num_uses()

        user_num_uses_rule = self.validate_user_num_uses(user=user)
        if isinstance(user_num_uses_rule, PromoCodeUser):
            user_num_uses_rule.num_uses += 1
            user_num_uses_rule.save()

        self.coupon.num_uses += 1
        self.coupon.save()
        self.cart.promo_code = self.coupon
        self.cart.save()
