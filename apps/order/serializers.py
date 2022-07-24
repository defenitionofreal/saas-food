from rest_framework import serializers

from apps.order.services.cart_helper import CartHelper
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


class CartHelperSerializer(serializers.ModelSerializer):
    # model fields

    items = ItemsSerializer(read_only=True, many=True)
    delivery = DeliveryInfoCustomerSerializer(read_only=True, many=False)

    # property methods

    get_total_cart = serializers.SerializerMethodField()
    get_total_cart_after_sale = serializers.SerializerMethodField()
    get_sale = serializers.SerializerMethodField()
    get_bonus_accrual = serializers.SerializerMethodField()
    get_delivery_price = serializers.SerializerMethodField()
    get_free_delivery_amount = serializers.SerializerMethodField()
    get_delivery_sale = serializers.SerializerMethodField()
    get_min_delivery_order_amount = serializers.SerializerMethodField()
    get_delivery_zone = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    def __init__(self, request, institution, **kwargs):
        self.cart = CartHelper(request=request, institution=institution)
        # model object is passed to init to support default serializer functionality
        cart_model_obj = self.cart.get_cart_obj()
        super().__init__(instance=cart_model_obj, data=serializers.empty, **kwargs)

    class Meta:
        model = Cart
        fields = (
            'id', 'customer', 'created_at', 'delivery', 'updated_at', 'items',
            'promo_code', 'customer_bonus', 'min_amount',

            # properties

            'get_total_cart', 'get_total_cart_after_sale',
            'get_sale', 'get_bonus_accrual',
            'get_delivery_price', 'get_free_delivery_amount',
            'get_delivery_sale', 'get_min_delivery_order_amount',
            'get_delivery_zone', 'final_price'
        )

    # ======= HELPER METHODS =======

    @property
    def is_empty(self):
        return self.cart.is_empty

    # ======= SERIALIZED FIELDS METHODS =======

    def get_get_total_cart(self, obj):
        return self.cart.get_total_cart

    def get_get_total_cart_after_sale(self, obj):
        return self.cart.get_total_cart_after_sale

    def get_get_sale(self, obj):
        return self.cart.get_sale

    def get_get_bonus_accrual(self, obj):
        return self.cart.get_bonus_accrual

    def get_get_delivery_price(self, obj):
        return self.cart.get_delivery_price

    def get_get_free_delivery_amount(self, obj):
        return self.cart.get_free_delivery_amount

    def get_get_delivery_sale(self, obj):
        return self.cart.get_delivery_sale

    def get_get_min_delivery_order_amount(self, obj):
        return self.cart.get_min_delivery_order_amount

    def get_get_delivery_zone(self, obj):
        return self.cart.get_delivery_zone

    def get_final_price(self, obj):
        return self.cart.final_price


# is not used anywhere
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
