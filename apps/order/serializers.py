from rest_framework import serializers

from apps.base.serializers import SimpleUserSerializer
from apps.showcase.serializers import SimpleInstitutionSerializer
from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer
from apps.company.services.validate_institution import validate_institution_list
from apps.product.serializers import SimpleModifierPriceSerializer, \
    SimpleAdditiveSerializer
from apps.order.models import Cart, CartItem, PromoCode, Bonus, UserBonus
from apps.delivery.serializers import CartDeliveryInfoSerializer
from apps.order.services.bonus_helper import BonusHelper


class ItemsSerializer(serializers.ModelSerializer):
    modifier = SimpleModifierPriceSerializer(read_only=True)
    additives = SimpleAdditiveSerializer(read_only=True, many=True)
    item_title = serializers.SlugRelatedField(source="item", slug_field="title", read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "cart", "item_title", "modifier", "additives", "quantity",
                  "get_item_price", "get_total_item_price", "item_hash")


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


# =========
class SimplePromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields = ["title", "code", "code_type", "sale"]


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    institution = SimpleInstitutionSerializer(read_only=True, many=False)
    promo_code = SimplePromoCodeSerializer(read_only=True, many=False)
    customer = SimpleUserSerializer(read_only=True, many=False)
    items = serializers.SerializerMethodField(read_only=True)
    delivery_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id', 'institution', 'customer', 'delivery_info',
            'payment_type', 'items', 'promo_code', 'customer_bonus',
            'min_amount',

            'get_total_cart', 'get_total_with_sale',
            'get_promo_code_sale',
            'get_bonus_accrual', 'get_bonus_write_off',

            'get_delivery_price', 'get_free_delivery_amount',
            'get_delivery_sale', 'get_min_delivery_order_amount',
            'get_final_sale', 'final_price',

            'comment', 'created_at', 'updated_at', 'confirmed_date',
            "code", "status", "paid"
        )

    def get_items(self, instance) -> ItemsSerializer:
        items = instance.products_cart.all()
        serializer = ItemsSerializer(items, read_only=True, many=True)
        return serializer.data

    def get_delivery_info(self, instance) -> CartDeliveryInfoSerializer:
        delivery_info = instance.delivery
        serializer = CartDeliveryInfoSerializer(delivery_info, read_only=True)
        return serializer.data
