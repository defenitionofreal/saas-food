from rest_framework import serializers
from apps.product.models import Category, Additive, Sticker


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


class StickerSerializer(serializers.ModelSerializer):
    """ Sticker serializer """

    class Meta:
        model = Sticker
        exclude = ['institution']
