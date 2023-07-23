from rest_framework import serializers

from apps.company.models import Institution, Banner
from apps.company.serializers import BannerSerializer
from apps.product.models import Product, Sticker
from apps.product.serializers import ProductSerializer, CategorySerializer


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


class ProductDetailSerializer(ProductSerializer):
    institutions = SimpleInstitutionSerializer(many=True, read_only=True)


class CategoryBasicSerializer(CategorySerializer):
    pass


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        exclude = ("link", "link_text", "user", "promo_code", "institutions",
                   "products")


class BannerDetailSerializer(BannerSerializer):
    pass

