from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import OrderItem, Order, Cart, CartItem, PromoCode, Bonus


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = (
            'id', 'customer', 'created_at', 'updated_at', 'items',
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
