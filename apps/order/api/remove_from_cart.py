from rest_framework.views import APIView
from rest_framework.response import Response
from apps.order.api.cart_from_request import get_cart_from_request
from apps.order.serializers import CartSerializer


class RemoveFromCartAPIView(APIView):
    """
    Remove product from cart
    - if auth look for a cart tied to a user
    - if not auth look for a cart tied to a session cart id
    - bottom logic looks for a product and rm it
    """

    def post(self, request, domain, product_slug):
        cart = get_cart_from_request(request, domain)

        if not cart:
            return Response({"detail": "Don't have a cart"})

        cart.remove_product_by_slug(product_slug)
        serializer = CartSerializer(cart, context={"request": request})

        return Response(serializer.data)
