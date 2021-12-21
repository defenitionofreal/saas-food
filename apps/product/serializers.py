from rest_framework import serializers
from apps.product.models import Category, Additive


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
