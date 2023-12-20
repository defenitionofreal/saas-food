from rest_framework import serializers

from apps.company.models import Institution, Banner
from apps.company.serializers import BannerSerializer
from apps.product.models import Product, Sticker
from apps.product.serializers import (
    ProductSerializer, CategorySerializer, NutritionalValueSerializer,
    WeightSerializer, CategoryAdditiveSerializer, ModifierPriceSerializer,
    ModifierSerializer
)


class OpenHoursSerializer(serializers.Serializer):
    is_open = serializers.BooleanField()


class SimpleInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "title"]


class StickerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sticker
        fields = ['id', 'color', 'text_color', 'title', 'is_active']


class ProductListSerializer(serializers.ModelSerializer):

    stickers = StickerListSerializer(read_only=True, many=True)
    # images todo

    class Meta:
        model = Product
        fields = ['id', 'institutions', 'category', 'title', 'slug', 'price',
                  'old_price', 'stickers', 'images', 'row']


class CustomModifiersSerializer(serializers.Serializer):
    modifier_id = serializers.IntegerField(read_only=True)
    modifier_title = serializers.CharField(read_only=True)
    price = ModifierPriceSerializer(read_only=True, allow_null=True)
    nutrition = NutritionalValueSerializer(read_only=True, allow_null=True)
    weight = WeightSerializer(read_only=True, allow_null=True)


class ProductDetailSerializer(ProductSerializer):
    additives = CategoryAdditiveSerializer(many=True, read_only=True, allow_null=True)
    modifiers = serializers.SerializerMethodField(read_only=True)
    nutrition = NutritionalValueSerializer(read_only=True, allow_null=True)
    weight = WeightSerializer(read_only=True, allow_null=True)

    def get_modifiers(self, instance) -> CustomModifiersSerializer(many=True):
        modifiers = instance.modifiers.all()
        data = [
            {"modifier_id": modifier.id,
             "modifier_title": modifier.title,
             "price": modifier.price(instance.id),
             "nutrition": modifier.nutrition(instance.id),
             "weight": modifier.weight(instance.id)}
            for modifier in modifiers
        ]
        return CustomModifiersSerializer(data, many=True).data


class CategoryBasicSerializer(CategorySerializer):
    pass


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        exclude = ("link", "link_text", "user", "promo_code", "institutions",
                   "products")


class BannerDetailSerializer(BannerSerializer):
    pass

