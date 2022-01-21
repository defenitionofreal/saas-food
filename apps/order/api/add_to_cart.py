from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem

from apps.base.authentication import JWTAuthentication


class AddToCartAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug):

        institution = Institution.objects.get(domain=domain)
        product = get_object_or_404(Product, slug=product_slug)
        user = self.request.user
        if user.is_authenticated and user.is_customer:
            user = user
        else:
            # make it that guest user can create cart
            # user = ?
            return Response(
                {"detail": "Authorize to add product to an order."})

        cart, cart_created = Cart.objects.get_or_create(
            institution=institution, customer=user)

        cart_item, cart_item_created = CartItem.objects.get_or_create(
            customer=user,
            product=product,
            cart=cart
        )

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
