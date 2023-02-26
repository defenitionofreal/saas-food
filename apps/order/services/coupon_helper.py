from apps.order.models import PromoCodeUser
from rest_framework.response import Response
from rest_framework import status
import datetime


class CouponHelper:
    """
    Main coupon class with all needed funcs and counts
    """

    def __init__(self, coupon, cart, user):
        self.coupon = coupon
        self.cart = cart
        self.user = user

    def _is_not_cart_coupon(self) -> bool:
        if self.cart.promo_code is None:
            return True
        return False

    def _is_coupon_active(self) -> bool:
        if self.coupon.is_active:
            return True
        return False

    # RULES
    def coupon_with_bonus_rule(self) -> Response:
        if self.cart.customer_bonus is not None:
            bonus = self.cart.institution.bonuses.filter(is_active=True).first()
            if bonus and bonus.is_promo_code is False:
                return Response(
                    {"detail": "Use promo code with bonuses is not allowed."},
                    status=status.HTTP_400_BAD_REQUEST)

    def sale_rule(self) -> Response:
        """ Not allowing to write off more than a final price """
        if self.coupon.code_type == 'absolute' and (
                self.cart.get_total_cart - self.coupon.sale) <= 0:
            return Response(
                {"detail": f"Sale is bigger: {self.cart.get_total_cart}"},
                status=status.HTTP_400_BAD_REQUEST)

        if self.coupon.code_type == 'percent' and self.coupon.sale > 100:
            return Response({"detail": "Sale is bigger 100%"},
                            status=status.HTTP_400_BAD_REQUEST)

    def total_cart_rule(self) -> Response:
        """
        Not allowing to use coupon if min coupon cart price < actual cart total
        """
        if self.coupon.cart_total is not None:
            if self.cart.get_total_cart < self.coupon.cart_total:
                return Response({"detail": f"Cart price has to be more {self.coupon.cart_total}"},
                                status=status.HTTP_400_BAD_REQUEST)

    def dates_rule(self) -> Response:
        """
        Not allowing to use coupon sooner or later from actual dates
        """
        today = datetime.datetime.now().date()
        if self.coupon.date_start is not None:
            if today < self.coupon.date_start:
                return Response({"detail": f"Code period not started yet"},
                                status=status.HTTP_400_BAD_REQUEST)

        if self.coupon.date_finish is not None:
            if today >= self.coupon.date_finish:
                return Response({"detail": f"Code period expired"},
                                status=status.HTTP_400_BAD_REQUEST)

    def tied_categories_rule(self) -> Response:
        if self.coupon.categories.all() and not self.coupon.products.all():
            x = set(self.cart.items.values_list('item__category', flat=True))
            y = set(self.coupon.categories.values_list(
                'promocode__categories__slug', flat=True))
            if not x.intersection(y):
                return Response({"detail": "No categories tied with coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

    def tied_products_rule(self) -> Response:
        if self.coupon.products.all() and not self.coupon.categories.all():
            x = set(self.cart.items.values_list('item__slug', flat=True))
            y = set(self.coupon.products.values_list(
                'promocode__products__slug', flat=True))
            if not x.intersection(y):
                return Response({"detail": "No products tied with coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

    def tied_products_and_categories_together_rule(self) -> Response:
        if self.coupon.products.all() and self.coupon.categories.all():
            coupon_items = []
            coupon_categories = self.coupon.categories.all()
            coupon_products = self.coupon.products.values_list("slug",
                                                               flat=True)
            cart_items = self.cart.items.values_list("item__slug",
                                                     flat=True)
            for category in coupon_categories:
                for product in category.products.values_list("slug",
                                                             flat=True):
                    coupon_items.append(product)
            for p in coupon_products:
                coupon_items.append(p)

            is_included = any(item in coupon_items for item in cart_items)

            if not is_included:
                return Response({"detail": "No items tied with coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

    def num_uses_rule(self):
        if self.coupon.code_use is not None:
            if self.coupon.num_uses >= self.coupon.code_use:
                return Response({"detail": "Max level exceeded for coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

    def user_num_uses_rule(self) -> [Response, PromoCodeUser]:
        if self.user.is_authenticated and self.coupon.code_use_by_user is not None:
            coupon_per_user, _ = PromoCodeUser.objects.get_or_create(
                code=self.coupon, user=self.user)
            if coupon_per_user.num_uses >= self.coupon.code_use_by_user:
                return Response({
                    "detail": "User's max level exceeded for coupon."},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return coupon_per_user

    def main(self) -> Response:
        coupon_with_bonus_rule = self.coupon_with_bonus_rule()
        sale_rule = self.sale_rule()
        total_cart_rule = self.total_cart_rule()
        dates_rule = self.dates_rule()
        tied_categories_rule = self.tied_categories_rule()
        tied_products_rule = self.tied_products_rule()
        tied_products_and_categories_together_rule = self.tied_products_and_categories_together_rule()
        num_uses_rule = self.num_uses_rule()
        user_num_uses_rule = self.user_num_uses_rule()

        if self._is_not_cart_coupon():
            if coupon_with_bonus_rule is not None:
                return coupon_with_bonus_rule
            if self._is_coupon_active():
                if sale_rule is not None:
                    return sale_rule
                elif total_cart_rule is not None:
                    return total_cart_rule
                elif dates_rule is not None:
                    return dates_rule
                elif tied_categories_rule is not None:
                    return tied_categories_rule
                elif tied_products_rule is not None:
                    return tied_products_rule
                elif tied_products_and_categories_together_rule is not None:
                    return tied_products_and_categories_together_rule
                elif num_uses_rule is not None:
                    return num_uses_rule
                elif isinstance(user_num_uses_rule, Response):
                    return user_num_uses_rule
                else:
                    if isinstance(user_num_uses_rule, PromoCodeUser):
                        user_num_uses_rule.num_uses += 1
                        user_num_uses_rule.save()
                    self.coupon.num_uses += 1
                    self.coupon.save()
                    self.cart.promo_code = self.coupon
                    self.cart.save()
                    return Response({"detail": "Code successfully added."},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Code is not active."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Promo code already applied."},
                            status=status.HTTP_400_BAD_REQUEST)
