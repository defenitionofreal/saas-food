from rest_framework.request import Request
from rest_framework.response import Response
from apps.order.models import Cart
from apps.company.models import Institution, MinCartCost
from django.conf import settings

class CartServiceException(Exception):
    """Cart service exception."""


class CartService:
    """Service for works with cart."""
    def get_cart(self, request: Request, domain: str) -> Cart:
        institution = Institution.objects.get(domain=domain)
        cart_cost = MinCartCost.objects.filter(institution=institution).first()
        min_amount = cart_cost.cost if cart_cost else None

        # User is authorized
        if request.user and request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                institution=institution,
                customer=request.user,
                defaults={"min_amount": min_amount},
            )
            return cart

        # User is not authorized
        if settings.CART_SESSION_ID not in request.session:
            raise CartServiceException("Cart does not exist. (session cart)")

        cart, _ = Cart.objects.get_or_create(
            institution=institution,
            session_id=request.session[settings.CART_SESSION_ID],
            defaults={"min_amount": min_amount},
        )
        return cart

    def update_cart(self, request: Request, domain: str) -> Cart:
        cart = self.get_cart(request, domain)



        return cart

"""
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

"""