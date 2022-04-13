from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution, MinCartCost
from apps.order.models import Cart
from apps.order.serializers import CartSerializer

from django.conf import settings


class CartAPIView(APIView):
    """
    Cart Detail View:
    - if auth than check for session
     - if session cart than create user cart and move items from one to another
     - if no session cart or session than check for user cart or create one
    - if not auth
     - check for session cart but if no cart than raise it
    """
    # TODO: ?? если авторизованный и нет, то какой permission_class ??

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        session = self.request.session
        cart_cost = MinCartCost.objects.filter(institution=institution).first()

        if user.is_authenticated:
            if settings.CART_SESSION_ID in session:
                session_cart = Cart.objects.filter(
                    institution=institution,
                    session_id=session[settings.CART_SESSION_ID]).first()
                if session_cart:
                    cart, cart_created = Cart.objects.get_or_create(
                        institution=institution, customer=user)

                    for item in session_cart.items.all():
                        item.cart = cart
                        item.save()

                        # TODO: count and add products not correctly. fix it!
                        product_filter = cart.items.filter(product__slug=item.product.slug)
                        if product_filter.exists():
                            for v in product_filter:
                                v.quantity += 1
                                v.save()
                            # item.quantity += 1
                            # item.save()
                        else:
                            cart.items.add(item)
                            cart.save()

                    if session_cart.promo_code:
                        cart.promo_code = session_cart.promo_code
                        cart.save()
                    session_cart.delete()
                    del session[settings.CART_SESSION_ID]
                    #session.flush()
                else:
                    # if no session cart
                    cart, cart_created = Cart.objects.get_or_create(
                        institution=institution, customer=user)
            else:
                cart = Cart.objects.filter(institution=institution,
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
