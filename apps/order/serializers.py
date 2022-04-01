from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.order.models import OrderItem, Order, Cart, CartItem, PromoCode, Bonus


class ItemsSerializer(serializers.ModelSerializer):
    pass


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

    # def to_representation(self, instance):
    #     """
    #     """
    #     rep = super(CartSerializer, self).to_representation(instance)
    #     session = self.context["request"].session
    #
    #     for item in instance.items.all():
    #         #check = item.check_if_product_in_session(session)
    #         products = session.get("product_with_options")
    #         if products:
    #             if item.product.slug in products["product"].keys():
    #                 price = products["product"][item.product.slug]["price"]
    #                 additives_total = products["product"][item.product.slug]["additives_price"]
    #                 if "additives" in products["product"][item.product.slug]:
    #                     additives = [v for k, v in products["product"][item.product.slug]["additives"].items()
    #                                  if products["product"][item.product.slug]["additives"]]
    #                 else:
    #                     additives = []
    #                 if "modifiers" in products["product"][item.product.slug]:
    #                     modifiers = [v for v in products["product"][item.product.slug]["modifiers"].values()
    #                                  if products["product"][item.product.slug]["modifiers"]]
    #                 else:
    #                     modifiers = []
    #                 # выводит только 1 товар !!!
    #                 item_response = {item.product.slug: {"price": price,
    #                                                      "additives_total": additives_total,
    #                                                      "additives": additives,
    #                                                      "modifiers": modifiers}}
    #                 rep['items'] = item_response
    #                 rep['get_total_cart'] = (int(rep['items'][item.product.slug]["price"]) + int(rep['items'][item.product.slug]["additives_total"]))
    #             else:
    #                 pass
    #                 # update with products that not in session?
    #                 # print(rep['items'])
    #                 # rep['items'].update({i.product.slug: {"price": i.product.price}
    #                 #             for i in instance.items.all()})
    #         else:
    #             rep['items'] = {i.product.slug: {"price": i.product.price}
    #                             for i in instance.items.all()}
    #     return rep


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
