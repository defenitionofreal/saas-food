from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.delivery.models.enums import SaleType
from apps.order.api.cart_from_request import get_cart_from_request
from apps.order.models import PromoCode, PromoCodeUser, Bonus


class AddPromoCodeAPIView(APIView):
    """ Add coupon to cart """

    def post(self, request, domain, coupon):
        user = self.request.user
        code = coupon
        coupon: PromoCode = get_object_or_404(PromoCode, code=code)
        institution = Institution.objects.get(domain=domain)

        cart = get_cart_from_request(request, domain)
        total_cart_price = cart.get_total_cart
        coupon_sale = coupon.sale
        coupon_cart_total = coupon.cart_total

        try:
            if cart.promo_code is None:

                if cart.customer_bonus is not None:
                    bonus = Bonus.objects.filter(institution=institution).first()
                    if bonus and bonus.is_promo_code is False:
                        return Response({"detail": "Use promo code with bonuses is not allowed."},
                                        status=status.HTTP_400_BAD_REQUEST)

                if coupon.is_active is True:
                    if coupon.code_type == SaleType.ABSOLUTE and total_cart_price <= coupon_sale:
                        return Response({"detail": f"Sale is bigger: {total_cart_price}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if coupon.code_type == SaleType.PERCENT and coupon_sale > 100:
                        return Response({"detail": "Sale is bigger 100%"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if not coupon.can_be_used_by_cart_total(total_cart_price):
                        return Response({"detail": f"Total cart price have to be more {coupon_cart_total}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if not coupon.can_be_used_today_by_start_date:
                        return Response({"detail": f"Code period not started yet"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if not coupon.can_be_used_today_by_finish_date:
                        return Response({"detail": f"Code period expired"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if coupon.categories.all():
                        x = set(cart.items.values_list('product__category', flat=True))
                        y = set(coupon.categories.values_list('promocode__categories__slug', flat=True))
                        if not x.intersection(y):
                            return Response(
                                {"detail": "No categories tied with coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

                    if coupon.products.all():
                        x = set(cart.items.values_list('product__slug', flat=True))
                        y = set(coupon.products.values_list('promocode__products__slug', flat=True))
                        if not x.intersection(y):
                            return Response(
                                {"detail": "No products tied with coupon."},
                                status=status.HTTP_400_BAD_REQUEST)

                    if not coupon.has_num_uses_left:
                        return Response({"detail": "Max level exceeded for coupon."},
                                        status=status.HTTP_400_BAD_REQUEST)

                    coupon.increase_num_uses()

                    if user.is_authenticated:
                        coupon_per_user, created = PromoCodeUser.objects.get_or_create(code=coupon, user=user)
                        coupon_per_user: PromoCodeUser = coupon_per_user
                        if not coupon_per_user.can_use_this_code:
                            return Response({"detail": "User's max level exceeded for coupon."},
                                            status=status.HTTP_400_BAD_REQUEST)

                        coupon_per_user.increase_num_uses()

                    cart.promo_code = coupon
                    cart.save()

                    return Response({"detail": "Code successfully added."},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Code is not active."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Promo code already applied."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"})
