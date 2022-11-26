from rest_framework import serializers
from apps.delivery.models import (Delivery,
                                  DeliveryZoneFile,
                                  DeliveryInfo,
                                  DeliveryZone,
                                  DeliveryZoneСoordinates)
from apps.base.services.delete_file import delete_old_file
from apps.company.serializers import BasicInstitutionSerializer
from apps.location.serializers import AddressLinkCustomerSerializer


class DeliverySerializer(serializers.ModelSerializer):
    """ Delivery serializer """
    institution = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        exclude = ['user']

    def get_institution(self, instance):
        return [affiliate.title for affiliate in instance.institution.all()]


class DeliveryInfoSerializer(serializers.ModelSerializer):
    """ Delivery info serializer """

    class Meta:
        model = DeliveryInfo
        exclude = ['user', 'session_id']


class DeliveryZoneFileSerializer(serializers.ModelSerializer):
    """ Delivery zone upload .kml file serializer """

    class Meta:
        model = DeliveryZoneFile
        exclude = ['institution']

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class DeliveryZoneSerializer(serializers.ModelSerializer):
    """ delivery zone serializer """
    institution = BasicInstitutionSerializer(many=False)
    dz_coordinates = serializers.SlugRelatedField(many=True,
                                                  read_only=True,
                                                  slug_field="coordinates")

    class Meta:
        model = DeliveryZone
        fields = "__all__"


class DeliveryCustomerSerializer(serializers.ModelSerializer):
    """ Delivery serializer """

    class Meta:
        model = Delivery
        exclude = ['user', 'institution', 'is_active']


class DeliveryInfoCustomerSerializer(serializers.ModelSerializer):
    """ Delivery info serializer """
    address = AddressLinkCustomerSerializer(read_only=True, many=False)
    type = DeliveryCustomerSerializer(read_only=True, many=False)

    class Meta:
        model = DeliveryInfo
        exclude = ['user', 'session_id']


# class DeliveryZoneCoordinatesSerializer(serializers.ModelSerializer):
#     """ Delivery zone coordinates nested serializer """
#     zone = DeliveryZoneSerializer(many=False)
#
#     class Meta:
#         model = DeliveryZoneСoordinates
#         fields = "__all__"
