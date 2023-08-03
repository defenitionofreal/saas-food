from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer
from apps.product.models import (
    Category, Additive, Sticker, Modifier, ModifierPrice, Product,
    CategoryAdditive, Weight, NutritionalValue
)
from apps.company.services.validate_institution import validate_institution_list


class NutritionalValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = NutritionalValue
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", None)
        modifier = validated_data.get("modifier", None)

        if modifier and modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance = NutritionalValue.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", instance.product)
        modifier = validated_data.get("modifier", instance.modifier)

        if modifier and modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance.modifier = modifier
        instance.product = product
        instance.protein = validated_data.get('protein', instance.protein)
        instance.fats = validated_data.get('fats', instance.fats)
        instance.carbohydrates = validated_data.get('carbohydrates', instance.carbohydrates)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.save()

        return instance


class WeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weight
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", None)
        modifier = validated_data.get("modifier", None)

        if modifier and modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance = Weight.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", instance.product)
        modifier = validated_data.get("modifier", instance.modifier)

        if modifier and modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance.modifier = modifier
        instance.product = product
        instance.weight_unit = validated_data.get('weight_unit', instance.weight_unit)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.save()

        return instance


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
    additives_data = serializers.SerializerMethodField()

    class Meta:
        model = CategoryAdditive
        fields = "__all__"

    def get_additives_data(self, instance):
        qs = Additive.objects.filter(category=instance)
        ser = AdditiveSerializer(qs, many=True)
        return ser.data

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.context["request"].user)
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
        user = self.context["request"].user
        qs = Institution.objects.filter(user=user)
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

    price_data = serializers.SerializerMethodField()
    weight_data = serializers.SerializerMethodField()
    nutritional_data = serializers.SerializerMethodField()

    class Meta:
        model = Modifier
        fields = "__all__"

    def get_price_data(self, instance):
        qs = instance.modifiers_price.first()
        data = ModifierPriceSerializer(qs).data
        return data
    def get_weight_data(self, instance):
        qs = instance.weights.first()
        data = WeightSerializer(qs).data
        return data

    def get_nutritional_data(self, instance):
        qs = instance.nutritional_values.first()
        data = NutritionalValueSerializer(qs).data
        return data

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Modifier.objects.filter(user=user)
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


class ModifierPriceSerializer(serializers.ModelSerializer):
    """ Modifier Price serializer """

    class Meta:
        model = ModifierPrice
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", None)
        modifier = validated_data.get("modifier", None)

        if modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance = ModifierPrice.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        product_qs = Product.objects.filter(user=user)
        product = validated_data.get("product", instance.product)
        modifier = validated_data.get("modifier", instance.modifier)

        if modifier.user != user:
            raise ValidationError("Wrong modifier id.")

        if not product:
            raise ValidationError("Product is required.")

        if product.id not in product_qs.values_list("id", flat=True):
            raise ValidationError("Wrong product id.")

        instance.modifier = modifier
        instance.product = product
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer """
    additives = CategoryAdditiveSerializer(many=True, read_only=True)
    modifiers = ModifierSerializer(many=True, read_only=True)
    stickers = StickerSerializer(many=True, read_only=True)
    nutritional_value = serializers.SerializerMethodField()
    weight_value = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_nutritional_value(self, instance):
        qs = NutritionalValue.objects.filter(
            product_id=instance.id, modifier__isnull=True
        ).first()
        data = NutritionalValueSerializer(qs).data if qs else None
        return data

    def get_weight_value(self, instance):
        qs = Weight.objects.filter(
            product_id=instance.id, modifier__isnull=True
        ).first()
        data = WeightSerializer(qs).data if qs else None
        return data

    def slug_validation(self, data):
        """
        Check that the slug is unique for each institution.
        """
        slug = data.get("slug")
        institutions_data = data.get("institutions", [])
        msg = {"detail": "A product with this slug already exists."}
        if not self.instance:
            for institution in institutions_data:
                if Product.objects.filter(slug=slug, institutions__id=institution.id).exists():
                    raise ValidationError(msg)
        else:
            existing_institutions = set(self.instance.institutions.values_list("id", flat=True))
            for institution in institutions_data:
                if institution not in existing_institutions and Product.objects.filter(slug=slug, institutions__id=institution.id).exists():
                    raise ValidationError(msg)
        # return data

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
        self.slug_validation(validated_data)
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Product.objects.filter(user=user)
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


# Simple Serializers

class SimpleModifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modifier
        fields = ["title"]


class SimpleModifierPriceSerializer(serializers.ModelSerializer):
    modifier_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ModifierPrice
        fields = ["modifier_title", "price"]

    def get_modifier_title(self, instance) -> SimpleModifierSerializer:
        modifier = instance.modifier
        serializer = SimpleModifierSerializer(modifier, read_only=True)
        return serializer.data


class SimpleCategoryAdditiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryAdditive
        fields = ["title"]


class SimpleAdditiveSerializer(serializers.ModelSerializer):
    category = SimpleCategoryAdditiveSerializer(read_only=True)

    class Meta:
        model = Additive
        fields = ["category", "title", "price"]
