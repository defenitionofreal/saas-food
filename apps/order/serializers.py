from rest_framework import serializers

from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer
from apps.company.services.validate_institution import validate_institution_list
from apps.order.models import Cart, CartItem, PromoCode, Bonus, UserBonus
from apps.order.services.bonus_helper import BonusHelper
from apps.delivery.serializers import DeliveryInfoCustomerSerializer


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ("id", "cart", "item", "modifier", "additives", "quantity",
                  "get_product_price", "get_total_item_price", "item_hash")


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
            "type": instance.delivery.type.delivery_type if instance.delivery else None,
            "address": instance.delivery.address.address.city if instance.delivery else None,  # fixme: json ser
            "date": instance.delivery_date,  # todo: инфа должна быть в delivery_info ?
            "time_from": instance.time_from, # todo: инфа должна быть в delivery_info ?
            "time_till": instance.time_till  # todo: инфа должна быть в delivery_info ?
        }
        return delivery_info


class CartDashboardSerializer(serializers.ModelSerializer):
    """ Serializer of a Cart/Order for customers dashboard. """

    items_count = serializers.SerializerMethodField()
    institution_title = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id', 'institution_title', 'items_count', 'final_price',
            'created_at', 'updated_at', 'confirmed_date', "code", "status",
            "paid"
        )

    def get_items_count(self, instance):
        return int(instance.products_cart.all().count())

    def get_institution_title(self, instance):
        return instance.institution.title


class UserBonusSerializer(serializers.ModelSerializer):
    """Serializer for the Customers dashboard about his bonuses"""

    institution = serializers.CharField(source="institution.title")

    class Meta:
        model = UserBonus
        exclude = ("user", )


# ======== for organizations only ===========


class PromoCodeSerializer(serializers.ModelSerializer):
    """ Serializer for the promo code (Coupon) model. """

    class Meta:
        model = PromoCode
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.context["request"].user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = PromoCode.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class BonusSerializer(serializers.ModelSerializer):
    """ Serializer for the Bonus """

    class Meta:
        model = Bonus
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.context["request"].user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Bonus.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)
