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

from apps.order.api.serializers.cart_product import CartProductDeleteInputSerializer
from apps.order.models import CartProduct
from apps.order.serializers import CartSerializer
from apps.order.services import CartService


class CartProductAPIView(APIView):
    """
    Remove product from cart
    - if auth look for a cart tied to a user
    - if not auth look for a cart tied to a session cart id
    - bottom logic looks for a product and rm it
    """
    authentication_classes = [JWTAuthentication]

    def delete(self, request, domain):
        cart_service = CartService()
        cart = cart_service.get_cart(request, domain)

        serializer = CartProductDeleteInputSerializer(data=request.data, context={"cart": cart})
        serializer.is_valid(raise_exception=True)

        CartProduct.objects.filter(id=serializer.validated_data["cart_product"].id).delete()

        return Response(CartSerializer(instance=cart, context={"request": request}).data)


    def _get_institution(self, domain):
        return Institution.objects.get(domain=domain)
