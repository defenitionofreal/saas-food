from rest_framework.views import APIView
from rest_framework.response import Response

from apps.product.models import Product, Modifier, Additive
from django.conf import settings
from apps.base.authentication import JWTAuthentication
from apps.order.serializers import CartSerializer
from apps.order.services import CartService
from rest_framework import serializers


class CartProductInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects, required=True)
    quantity = serializers.IntegerField(default=1)
    modifiers = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Modifier.objects))
    additives = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Additive.objects))


class AddToCartAPIView(APIView):
    """
    Add product to cart view:
    - if auth get or create cart tied to a user
    - if not auth check for session id in session
     - if no id than generate one else get id
     - than get or create cart tied to a session id
    - bottom logic check products, counts quantity, adds to cart
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug=None):
        cart_service = CartService()
        cart = cart_service.get_cart(request, domain)

        cart_session_id = request.session.get(settings.CART_SESSION_ID)
        if cart_session_id != cart.session_id:
            request.session[settings.CART_SESSION_ID] = cart.session_id
            request.session.modified = True

        cart_product_data = CartProductInputSerializer(data=request.data)
        cart_product_data.is_valid(raise_exception=True)

        cart_service.add_product(cart, cart_product_data.validated_data)
        return Response(CartSerializer(instance=cart, context={"request": request}).data)

        # institution = Institution.objects.get(domain=domain)
        # product = get_object_or_404(Product, slug=product_slug)
        # user = self.request.user
        # session = self.request.session
        #
        # if user.is_authenticated:  # and user.is_customer
        #     cart, cart_created = Cart.objects.get_or_create(
        #         institution=institution, customer=user)
        #     cart_item, cart_item_created = CartItem.objects.get_or_create(
        #         product=product, cart=cart)
        # else:
        #     if not settings.CART_SESSION_ID in session:
        #         session[settings.CART_SESSION_ID] = _generate_cart_key()
        #     else:
        #         session[settings.CART_SESSION_ID]
        #     session.modified = True
        #
        #     cart, cart_created = Cart.objects.get_or_create(
        #         institution=institution, session_id=session[settings.CART_SESSION_ID])
        #     cart_item, cart_item_created = CartItem.objects.get_or_create(
        #         product=product, cart=cart)
        #
        # if cart_created is False:
        #     if cart.items.filter(product__slug=product.slug).exists():
        #         cart_item.quantity += 1
        #         cart_item.save()
        #         return Response({"detail": "Product quantity updated"})
        #     else:
        #         cart.items.add(cart_item)
        #         return Response({"detail": "New product added"})
        # else:
        #     cart.items.add(cart_item)
        #     return Response({"detail": "Cart created and product added"})
