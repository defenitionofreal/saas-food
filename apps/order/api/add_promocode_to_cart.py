from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.order.models import Cart, PromoCode, PromoCodeUser, Bonus

from django.conf import settings
import datetime


class AddPromoCodeAPIView(APIView):
    """ Add coupon to cart """

    def post(self, request, domain, coupon):
        today = datetime.datetime.now().date()
        user = self.request.user
        code = coupon
        coupon = get_object_or_404(PromoCode, code=code)
        institution = Institution.objects.get(domain=domain)
        session = self.request.session

        if user.is_authenticated:
            cart = Cart.objects.get(institution=institution, customer=user)
        else:
            if settings.CART_SESSION_ID in session:
                cart = Cart.objects.get(institution=institution,
                                        session_id=session[
                                            settings.CART_SESSION_ID])

        try:
            if cart.promo_code is None:

                if cart.customer_bonus is not None:
                    bonus = Bonus.objects.filter(institution=institution).first()
                    if bonus and bonus.is_promo_code is False:
                        return Response({"detail": "Use promo code with bonuses is not allowed."},
                                        status=status.HTTP_400_BAD_REQUEST)

                if coupon.is_active is True:
                    if coupon.code_type == 'absolute' and (cart.get_total_cart - coupon.sale) <= 0:
                        return Response({"detail": f"Sale is bigger: {cart.get_total_cart}"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if coupon.code_type == 'percent' and coupon.sale > 100:
                        return Response({"detail": "Sale is bigger 100%"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    if coupon.cart_total is not None:
                        if cart.get_total_cart < coupon.cart_total:
                            return Response({"detail": f"Total cart price have to be more {coupon.cart_total}"},
                                            status=status.HTTP_400_BAD_REQUEST)

                    if coupon.date_start is not None:
                        if today < coupon.date_start:
                            return Response({"detail": f"Code period not started yet"},
                                            status=status.HTTP_400_BAD_REQUEST)

                    if coupon.date_finish is not None:
                        if today >= coupon.date_finish:
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

                    if coupon.code_use is not None:
                        if coupon.num_uses >= coupon.code_use:
                            return Response({"detail": "Max level exceeded for coupon."},
                                            status=status.HTTP_400_BAD_REQUEST)
                        coupon.num_uses += 1
                        coupon.save()

                    if user.is_authenticated:
                        coupon_per_user, created = PromoCodeUser.objects.get_or_create(
                            code=coupon, user=user)
                        if coupon.code_use_by_user is not None:
                            if coupon_per_user.num_uses >= coupon.code_use_by_user:
                                return Response({
                                    "detail": "User's max level exceeded for coupon."},
                                status=status.HTTP_400_BAD_REQUEST)
                        coupon_per_user.num_uses += 1
                        coupon_per_user.save()

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
