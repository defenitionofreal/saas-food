from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import OrderItem, Cart, CartItem
from apps.order.serializers import CartSerializer, CartItemSerializer

from apps.base.authentication import JWTAuthentication


class AddToCartAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug):

        institution = Institution.objects.get(domain=domain)
        item = get_object_or_404(Product, slug=product_slug)
        user = self.request.user
        if user.is_authenticated and user.is_customer:
            user = user
        else:
            # make it that guest user can create cart
            # user = ?
            return Response(
                {"detail": "Authorize to add product to an order."})


        cart_item, cart_item_created = CartItem.objects.get_or_create(
            customer=user,
            product=item
        )

        cart = Cart.objects.filter(institution=institution, customer=user)
        if cart.exists():
            cart = cart[0]
            if cart.items.filter(product__slug=item.slug).exists():
                cart_item.quantity += 1
                cart_item.save()
                return Response({"detail": "product quantity updated"})
            else:
                cart.items.add(cart_item)
                return Response({"detail": "new product added"})
        else:
            cart = Cart.objects.create(institution=institution, customer=user)
            cart.items.add(cart_item)
            return Response({"detail": "new cart created and product added"})