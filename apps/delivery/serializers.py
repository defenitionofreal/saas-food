from rest_framework import serializers

from apps.company.models import Institution
from apps.company.services.validate_institution import validate_institution_list
from apps.delivery.models import (
    DeliveryTypeRule, DeliveryZone, CartDeliveryInfo, CustomerAddress,
    InstitutionAddress, YandexGeocoderToken
)
from apps.company.serializers import BasicInstitutionSerializer


class YandexGeocoderTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = YandexGeocoderToken
        fields = "__all__"
        read_only_fields = ["user"]

    def save(self, **kwargs):
        user = self.context["request"].user
        kwargs["user"] = user
        return super().save(**kwargs)


class DeliveryTypeRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryTypeRule
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = DeliveryTypeRule.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=False
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class CustomerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = "__all__"


class InstitutionAddressSerializer(serializers.ModelSerializer):
    institution = BasicInstitutionSerializer(many=False)

    class Meta:
        model = InstitutionAddress
        fields = "__all__"


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = DeliveryZone.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=False
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class CartDeliveryInfoSerializer(serializers.ModelSerializer):
    type = DeliveryTypeRuleSerializer(read_only=True)
    zone = DeliveryZoneSerializer(read_only=True)
    customer_address = CustomerAddressSerializer(read_only=True)
    institution_address = InstitutionAddressSerializer(read_only=True)

    class Meta:
        model = CartDeliveryInfo
        fields = "__all__"
