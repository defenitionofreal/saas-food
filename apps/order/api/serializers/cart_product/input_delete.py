from rest_framework import serializers

from apps.order.models import CartProduct


class CartProductDeleteInputSerializer(serializers.Serializer):
    cart_product = serializers.PrimaryKeyRelatedField(queryset=CartProduct.objects, required=True)

    def validate_cart_product(self, cart_product):
        if cart_product.cart != self.context["cart"]:
            raise serializers.ValidationError("Product not found")
        return cart_product
