from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem

from apps.base.authentication import JWTAuthentication


class RemoveFromCartAPIView(APIView):
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

        cart = Cart.objects.filter(institution=institution, customer=user)
        if cart.exists():
            cart = cart[0]
            if cart.items.filter(product__slug=product.slug).exists():
                cart_item = CartItem.objects.get(product=product,
                                                 customer=user)
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
