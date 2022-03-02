from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem

from apps.base.authentication import JWTAuthentication
from django.conf import settings


class RemoveFromCartAPIView(APIView):
    """
    Remove product from cart
    - if auth look for a cart tied to a user
    - if not auth look for a cart tied to a session cart id
    - bottom logic looks for a product and rm it
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug):

        institution = Institution.objects.get(domain=domain)
        product = get_object_or_404(Product, slug=product_slug)
        user = self.request.user
        session = self.request.session

        if user.is_authenticated:  # and user.is_customer
            cart = Cart.objects.filter(institution=institution, customer=user)
        else:
            if not settings.CART_SESSION_ID in session:
                return Response(
                    {"detail": "Cart does not exist. (session cart)"})
            cart = Cart.objects.filter(institution=institution,
                                       session_id=session[settings.CART_SESSION_ID])

        if cart.exists():
            cart = cart[0]
            if cart.items.filter(product__slug=product.slug).exists():
                cart_item = CartItem.objects.get(product=product,
                                                 cart=cart)
                                                 #customer=user)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart.items.remove(cart_item)
                return Response({"detail": "Product quantity updated"})
            else:
                return Response({"detail": "This product not in a cart"})
        else:
            return Response({"detail": "Don't have a cart"})
