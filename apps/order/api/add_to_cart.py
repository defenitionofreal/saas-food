from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem

from apps.order.services.generate_cart_key import _generate_cart_key
from django.conf import settings


class AddToCartAPIView(APIView):
    """
    Add product to cart view:
    - if auth get or create cart tied to a user
    - if not auth check for session id in session
     - if no id than generate one else get id
     - than get or create cart tied to a session id
    - bottom logic check products, counts quantity, adds to cart
    """

    def post(self, request, domain, product_slug):

        institution = Institution.objects.get(domain=domain)
        product = get_object_or_404(Product, slug=product_slug)
        user = self.request.user
        session = self.request.session

        if user.is_authenticated:  # and user.is_customer
            cart, cart_created = Cart.objects.get_or_create(
                institution=institution, customer=user)
            cart_item, cart_item_created = CartItem.objects.get_or_create(
                product=product, cart=cart)
        else:
            if not settings.CART_SESSION_ID in session:
                session[settings.CART_SESSION_ID] = _generate_cart_key()
            else:
                session[settings.CART_SESSION_ID]
            session.modified = True

            cart, cart_created = Cart.objects.get_or_create(
                institution=institution, session_id=session[settings.CART_SESSION_ID])
            cart_item, cart_item_created = CartItem.objects.get_or_create(
                product=product, cart=cart)

        if cart_created is False:
            if cart.items.filter(product__slug=product.slug).exists():
                cart_item.quantity += 1
                cart_item.save()
                return Response({"detail": "Product quantity updated"})
            else:
                cart.items.add(cart_item)
                return Response({"detail": "New product added"})
        else:
            cart.items.add(cart_item)
            return Response({"detail": "Cart created and product added"})
