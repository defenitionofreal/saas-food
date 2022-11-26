from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import Cart, CartItem, PromoCode, Bonus, Order
from apps.order.services.bonus_helper import BonusHelper
from apps.delivery.serializers import DeliveryInfoCustomerSerializer


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity", "get_total_item_price")


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    items = ItemsSerializer(read_only=True, many=True)
    #delivery = DeliveryInfoCustomerSerializer(read_only=True, many=False)
    max_bonus_write_off = serializers.SerializerMethodField()
    institution = serializers.SerializerMethodField()
    customer_info = serializers.SerializerMethodField()
    delivery_info = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id', 'institution',
            'customer_info', 'delivery_info', 'payment_type', 'items',
            'promo_code', 'customer_bonus', 'min_amount', 'get_total_cart',
            'get_total_cart_after_sale', 'get_sale',
            'get_bonus_accrual', 'max_bonus_write_off',
            'get_delivery_price', 'get_free_delivery_amount',
            'get_delivery_sale', 'get_min_delivery_order_amount',
            'get_delivery_zone', 'final_price', 'comment',
            'created_at', 'updated_at', 'confirmed_date', "code", "status",
            "paid"
        )

    def get_max_bonus_write_off(self, instance):
        bonus = BonusHelper(0, instance, instance.customer)
        return bonus.max_write_off_amount()

    def get_institution(self, instance):
        return instance.institution.title

    def get_customer_info(self, instance):
        customer_info = {
            "customer_uuid": instance.customer.id if instance.customer else "guest",
            "order_customer_name": instance.name,
            "order_customer_phone": str(instance.phone),
            "order_customer_email": instance.email
        }
        return customer_info

    def get_delivery_info(self, instance):
        delivery_info = {
            "type": instance.delivery.delivery_type.delivery_type if instance.delivery else None,
            "address": instance.delivery.address.address if instance.delivery else None,
            "date": instance.delivery_date,
            "time_from": instance.time_from,
            "time_till": instance.time_till
        }
        return delivery_info


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
        fields = ["id", "institution_name", "payment_type", "name", "phone",
                  "comment", "delivery", "items", "total", "coupon_sale",
                  "bonus_write_off", "total_after_sale", "delivery_cost",
                  "delivery_sale", "bonus_accrual", "final_price",
                  "code", "status", "paid"]


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
