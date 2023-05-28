from rest_framework import serializers
from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer
from apps.product.models import (
    Category, Additive, Sticker, Modifier, ModifierPrice, Product,
    CategoryAdditive
)
from apps.company.services.validate_institution import validate_institution_list


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer """

    class Meta:
        model = Category
        fields = ["id", "institutions", "title", "slug", "row", "is_active"]

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Category.objects.filter(user=user)
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


class CategoryAdditiveSerializer(serializers.ModelSerializer):
    """ Category Additive serializer """

    class Meta:
        model = CategoryAdditive
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = CategoryAdditive.objects.filter(user=user)
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


class AdditiveSerializer(serializers.ModelSerializer):
    """ Additive serializer """

    class Meta:
        model = Additive
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Additive.objects.filter(user=user)
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


class StickerSerializer(serializers.ModelSerializer):
    """ Sticker serializer """

    class Meta:
        model = Sticker
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Sticker.objects.filter(user=user)
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


class ModifierSerializer(serializers.ModelSerializer):
    """ Modifier serializer """

    class Meta:
        model = Modifier
        exclude = ['user']


class ModifierPriceSerializer(serializers.ModelSerializer):
    """ Modifier Price serializer """

    class Meta:
        model = ModifierPrice
        exclude = ['user']


class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer """

    class Meta:
        model = Product
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_stickers(self, value):
        """
        Check that product could have only not more than 3 stickers
        """
        if len(value) > 3:
            raise serializers.ValidationError(
                {"detail": "Maximum 3 stickers allowed."}
            )
        return value

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Sticker.objects.filter(user=user)
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
            {"title": mod.title, "price": p.price}
            for mod in instance.modifiers.all()
            for p in mod.modifiers_price.all()
            if p.product.id == instance.id and p.modifier.id == mod.id
        ]
        return rep


class ProductListSerializer(serializers.ModelSerializer):
    """ Product list serializer """

    class Meta:
        model = Product
        fields = ['id', 'institution', 'category', 'title', 'slug', 'price',
                  'old_price', 'sticker', 'row', 'images']

    def validate_sticker(self, value):
        """
        Check that product could have
        only not more than 3 stickers
        """
        if len(value) > 3:
            raise serializers.ValidationError("Maximum number should be 3")
        return value
