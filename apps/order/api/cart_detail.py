import json

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution, MinCartCost
from apps.order.models import Cart
from apps.order.serializers import CartSerializer
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings
from django.db.models import F


class CartAPIView(APIView):
    """
    Cart Detail View:
    - if auth than check for session
     - if session cart than create user cart and move items from one to another
     - if no session cart or session than check for user cart or create one
    - if not auth
     - check for session cart but if no cart than raise it
    """

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        session = self.request.session
        cart_cost = MinCartCost.objects.filter(institution=institution).first()

        if user.is_authenticated:
            if settings.CART_SESSION_ID in session:
                cart = Cart.objects.filter(
                    institution=institution,
                    session_id=session[settings.CART_SESSION_ID]).first()
                if cart:
                    if not cart.customer:
                        cart.customer = user
                        cart.save()
                    # cart, cart_created = Cart.objects.get_or_create(
                    #     institution=institution, customer=user)
                    #
                    # for session_item in session_cart.items.all():
                    #     session_item.cart = cart
                    #     session_item.save()
                    #
                    #     cart_item_duplicates = cart.items.filter(product__slug=session_item.product["slug"])
                    #     if cart_item_duplicates.exists():
                    #         for i in cart_item_duplicates:
                    #             i.quantity = F("quantity") + session_item.quantity
                    #             i.save(update_fields=("quantity",))
                    #     else:
                    #         cart.items.add(session_item)
                    #         cart.save()
                    #
                    # if session_cart.promo_code:
                    #     cart.promo_code = session_cart.promo_code
                    #     cart.save()
                    #
                    # session_cart.delete()
                    # del session[settings.CART_SESSION_ID]
                    # #session.flush()
                else:
                    # if no session cart
                    cart, cart_created = Cart.objects.get_or_create(
                        institution=institution,
                        customer=user,
                        session_id=session[settings.CART_SESSION_ID])
            else:
                session[settings.CART_SESSION_ID] = _generate_cart_key()
                cart = Cart.objects.filter(institution=institution,
                                           session_id=session[
                                               settings.CART_SESSION_ID],
                                           customer=user).first()
                if not cart:
                    return Response({"detail": "Cart does not exist. (auth cart)"})
        else:
            if not settings.CART_SESSION_ID in session:
                return Response({"detail": "Cart does not exist. (session cart)"})

            cart = Cart.objects.get(institution=institution,
                                    session_id=session[settings.CART_SESSION_ID])

        try:
            if cart_cost:
                cart.min_amount = cart_cost.cost
                cart.save()

            if cart.items.exists():
                serializer = CartSerializer(cart, context={"request": request})
                return Response(serializer.data)
            else:
                return Response({"detail": "Cart is empty."})
        except Exception as e:
            return Response({"detail": f"{e}"})
