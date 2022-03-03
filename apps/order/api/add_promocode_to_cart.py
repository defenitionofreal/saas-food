from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem, PromoCode, PromoCodeUser, Bonus

from apps.base.authentication import JWTAuthentication
from django.conf import settings
from decimal import Decimal
import datetime


class AddPromoCodeAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain):
        today = datetime.datetime.now().date()
        user = self.request.user
        code = self.request.query_params.get("code")
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
                        return Response({"detail": "Use promo code with bonuses is not allowed."})

                if coupon.is_active is True:
                    if coupon.code_type == 'absolute' and (cart.get_total_cart - coupon.sale) <= 0:
                        return Response({"detail": f"Sale is bigger: {cart.get_total_cart}"})
                    if coupon.code_type == 'percent' and coupon.sale > 100:
                        return Response({"detail": "Sale is bigger 100%"})

                    if coupon.cart_total is not None:
                        if cart.get_total_cart < coupon.cart_total:
                            return Response({"detail": f"Total cart price have to be more {coupon.cart_total}"})

                    # if delivery_free

                    if coupon.date_start is not None:
                        if coupon.date_start > today:  # <
                            return Response({"detail": f"Code period not started yet"})

                    if coupon.date_finish is not None:
                        if coupon.date_finish >= today:
                            return Response({"detail": f"Code period expired"})

                    # if coupon.categories.all():
                    #     for i in cart.items.all():
                    #         if not i.product.category in coupon.categories.all():
                    #             return Response({"detail": "No categories linked to the code."})
                    #
                    # if coupon.products.all():
                    #     for i in cart.items.all():
                    #         if not i.product in coupon.products.all():
                    #             return Response({"detail": "No products linked to the code."})

                    if coupon.code_use is not None:
                        if coupon.num_uses >= coupon.code_use:
                            return Response({"detail": "Max level exceeded for coupon."})
                        coupon.num_uses += 1
                        coupon.save()

                    if user.is_authenticated:
                        coupon_per_user, created = PromoCodeUser.objects.get_or_create(
                            code=coupon, user=user)
                        if coupon.code_use_by_user is not None:
                            if coupon_per_user.num_uses >= coupon.code_use_by_user:
                                return Response({
                                    "detail": "User's max level exceeded for coupon."})
                        coupon_per_user.num_uses += 1
                        coupon_per_user.save()

                    cart.promo_code = coupon
                    cart.save()
                    return Response({"detail": "Code successfully added."})
                else:
                    return Response({"detail": "Code is not active."})
            else:
                return Response({"detail": "Promo code already applied."})
        except Exception as e:
            return Response({"detail": f"{e}"})
