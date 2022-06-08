from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import Cart, CartItem, PromoCode, Bonus
from apps.delivery.serializers import DeliveryInfoCustomerSerializer


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity", "get_additives",
                  "get_modifiers", "get_total_item_price")


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    items = ItemsSerializer(read_only=True, many=True)
    delivery = DeliveryInfoCustomerSerializer(read_only=True, many=False)

    class Meta:
        model = Cart
        fields = (
            'id', 'customer', 'created_at', 'delivery', 'updated_at', 'items',
            'promo_code', 'customer_bonus', 'min_amount', 'get_total_cart',
            'get_total_cart_after_sale', 'get_sale', 'get_bonus_accrual'
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


# ======== for organizations only ===========


class PromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for the promo code (Coupon) model."""

    class Meta:
        model = PromoCode
        exclude = ['institution']


class BonusSerializer(serializers.ModelSerializer):
    """Serializer for the Bonus"""

    class Meta:
        model = Bonus
        exclude = ['institution']
