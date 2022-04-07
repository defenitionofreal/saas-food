from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, GenericAPIView

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem
from rest_framework import mixins
from apps.base.authentication import JWTAuthentication
from django.conf import settings
from http import HTTPStatus

from apps.order.api.serializers.cart_product import CartProductAddInputSerializer, CartProductDeleteInputSerializer
from apps.order.models import CartProduct
from apps.order.serializers import CartSerializer
from apps.order.services import CartService


class CartProductAPIView(APIView):
    """
    Get - get cart product from cart
    Post - add cart product to cart
    Delete - delete cart product from cart
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain):
        """Add product cart to cart."""
        cart_service = CartService()
        cart = cart_service.get_cart(request, domain)

        cart_session_id = request.session.get(settings.CART_SESSION_ID)
        if cart_session_id != cart.session_id:
            request.session[settings.CART_SESSION_ID] = cart.session_id
            request.session.modified = True

        cart_product_data = CartProductAddInputSerializer(data=request.data, context={"cart": cart})
        cart_product_data.is_valid(raise_exception=True)

        cart_service.add_product(cart, cart_product_data.validated_data)
        return Response(CartSerializer(instance=cart, context={"request": request}).data)


    def delete(self, request, domain):
        """Delete product cart from cart."""
        cart_service = CartService()
        cart = cart_service.get_cart(request, domain)

        serializer = CartProductDeleteInputSerializer(data=request.data, context={"cart": cart})
        serializer.is_valid(raise_exception=True)

        CartProduct.objects.filter(id=serializer.validated_data["cart_product"].id).delete()

        return Response(CartSerializer(instance=cart, context={"request": request}).data)
