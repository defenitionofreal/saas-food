from rest_framework import serializers


from apps.product.models import Product, Modifier, Additive


class CartProductAddInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects, required=True)
    quantity = serializers.IntegerField(default=1)
    modifiers = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Modifier.objects))
    additives = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Additive.objects))

    def validate_product(self, product):
        if product.institution != self.context["cart"].institution:
            raise serializers.ValidationError("Product not found")
        return product

    def validate_quantity(self, quantity):
        if quantity < 1:
            raise serializers.ValidationError("Quantity must be more than 0")
        return quantity

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self._validate_modifiers(attrs["product"], attrs["modifiers"])
        self._validate_additives(attrs["product"], attrs["additives"])
        return attrs

    def _validate_modifiers(self, product, modifiers) -> None:
        if not modifiers:
            return None
        wrong_modifiers = set(modifiers) - set(product.modifiers.all())

        if wrong_modifiers:
            raise serializers.ValidationError(
                "Wrong modifiers: {0}".format(", ".join((modifier.title for modifier in wrong_modifiers))),
            )

    def _validate_additives(self, product, additives) -> None:
        if not additives:
            return None

        return None
