from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import OrderItem, Order, Cart, CartItem


class CartSerializer(serializers.ModelSerializer):

    """Serializer for the Cart model."""

    #customer = UserSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = (
            'id', 'customer', 'created_at', 'updated_at', 'items',
            'promo_code', 'customer_bonus', 'min_amount'
        )

class CartItemSerializer(serializers.ModelSerializer):

    """Serializer for the CartItem model."""

    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id', 'cart', 'product', 'quantity'
        )


# class OrderItemSerializer(serializers.ModelSerializer):
#     """ Order item(s) serializer """
#     product = ProductSerializer()
#
#     class Meta:
#         model = OrderItem
#         fields = ['order', 'product', 'price', 'quantity']
#         #exclude = ['order']
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     """ Order serializer """
#     items = OrderItemSerializer(many=True)
#
#     class Meta:
#         model = Order
#         fields = '__all__'
