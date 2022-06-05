from rest_framework import serializers
from apps.delivery.models import (Delivery,
                                  DeliveryZoneFile,
                                  DeliveryInfo,
                                  DeliveryZone,
                                  DeliveryZoneСoordinates)
from apps.base.services.delete_file import delete_old_file
from apps.company.serializers import BasicInstitutionSerializer


class DeliverySerializer(serializers.ModelSerializer):
    """ Delivery serializer """

    class Meta:
        model = Delivery
        exclude = ['user']


class DeliveryInfoSerializer(serializers.ModelSerializer):
    """ Delivery info serializer """

    class Meta:
        model = DeliveryInfo
        exclude = ['user', 'type']


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

    class Meta:
        model = DeliveryZone
        fields = "__all__"


class DeliveryZoneCoordinatesSerializer(serializers.ModelSerializer):
    """ Delivery zone coordinates nested serializer """
    zone = DeliveryZoneSerializer(many=False)

    class Meta:
        model = DeliveryZoneСoordinates
        fields = "__all__"
