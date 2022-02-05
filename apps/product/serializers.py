from rest_framework import serializers
from apps.product.models import Category, Additive, Sticker, Modifier, \
    ModifierPrice, Product, CategoryAdditive


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer """

    class Meta:
        model = Category
        exclude = ['institution']


class AdditiveSerializer(serializers.ModelSerializer):
    """ Additive serializer """

    class Meta:
        model = Additive
        exclude = ['institution']


class CategoryAdditiveSerializer(serializers.ModelSerializer):
    """ Category Additive serializer """

    class Meta:
        model = CategoryAdditive
        exclude = ['institution']


class StickerSerializer(serializers.ModelSerializer):
    """ Sticker serializer """

    class Meta:
        model = Sticker
        exclude = ['institution']


class ModifierSerializer(serializers.ModelSerializer):
    """ Modifier serializer """

    class Meta:
        model = Modifier
        exclude = ['institution']


class ModifierPriceSerializer(serializers.ModelSerializer):
    """ Modifier Price serializer """

    class Meta:
        model = ModifierPrice
        exclude = ['institution', 'modifier']


class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer """

    class Meta:
        model = Product
        exclude = ['institution']
