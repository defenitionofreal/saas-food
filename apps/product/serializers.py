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

    def validate_sticker(self, value):
        """
        Check that product could have
        only not more than 3 stickers
        """
        if len(value) > 3:
            raise serializers.ValidationError("Maximum number should be 3")
        return value

    def to_representation(self, instance):
        """
        Return additives with nested dict of a
        additive category and additives in it.
        Also modifiers with the same logic.
        """
        rep = super(ProductSerializer, self).to_representation(instance)
        rep['additives'] = [{cat.title: {i.title: i.price
                                         for i in cat.category_additive.all()
                                         if i.category.id == cat.id}}
                            for cat in instance.additives.all()]
        rep['modifiers'] = [
            {mod.title: p.price for p in mod.modifiers_price.all()
             if p.product.id == instance.id and p.modifier.id == mod.id}
            for mod in instance.modifiers.all()]
        return rep
