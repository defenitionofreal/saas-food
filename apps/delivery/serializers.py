from rest_framework import serializers
from apps.delivery.models import  (
    DeliveryTypeRule, DeliveryZone, CartDeliveryInfo, CustomerAddress,
    InstitutionAddress
)
from apps.company.serializers import BasicInstitutionSerializer


class DeliveryTypeRuleSerializer(serializers.ModelSerializer):
    institutions = BasicInstitutionSerializer(many=True)

    class Meta:
        model = DeliveryTypeRule
        field = "__all__"


class CartDeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartDeliveryInfo
        field = "__all__"


class DeliveryZoneSerializer(serializers.ModelSerializer):
    """ delivery zone serializer """
    institutions = BasicInstitutionSerializer(many=True)

    class Meta:
        model = DeliveryZone
        fields = "__all__"


class CustomerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = "__all__"

class InstitutionAddressSerializer(serializers.ModelSerializer):
    institution = BasicInstitutionSerializer(many=False)

    class Meta:
        model = InstitutionAddress
        fields = "__all__"

