from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem

from apps.base.authentication import JWTAuthentication
from django.conf import settings
from http import HTTPStatus

from order.models import CartProduct


class CartProductAPIView(APIView):
    """
    Remove product from cart
    - if auth look for a cart tied to a user
    - if not auth look for a cart tied to a session cart id
    - bottom logic looks for a product and rm it
    """
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, domain, product_cart_id):
        CartProduct.objects.filter(id=product_cart_id, cart__institution__domain=domain).delete()

        return Response(status=HTTPStatus.NO_CONTENT)


    def _get_institution(self, domain):
        return Institution.objects.get(domain=domain)
