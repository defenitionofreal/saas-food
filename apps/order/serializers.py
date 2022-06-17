from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import Cart, CartItem, PromoCode, Bonus, Order
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
            'get_total_cart_after_sale', 'get_sale', 'get_bonus_accrual',
            'get_delivery_price', 'get_free_delivery_amount',
            'get_delivery_sale', 'get_min_delivery_order_amount',
            'get_delivery_zone',
            'final_price'
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


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for an Order model."""

    class Meta:
        model = Order
        fields = ["id", "payment_type", "name", "phone", "comment",
                  "delivery", "items", "total", "coupon_sale",
                  "bonus_write_off", "total_after_sale", "delivery_cost",
                  "delivery_sale", "bonus_accrual", "final_price", "paid"]


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
