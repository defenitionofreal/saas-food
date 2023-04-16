from rest_framework import serializers
from apps.location.models import Address, AddressLink
from apps.company.serializers import BasicInstitutionSerializer


class AddressSerializer(serializers.ModelSerializer):
    """ address serializer """

    class Meta:
        model = Address
        fields = "__all__"


class AddressLinkSerializer(serializers.ModelSerializer):
    """ address link serializer """
    address = AddressSerializer(many=False)
    institution = BasicInstitutionSerializer(many=False)

    class Meta:
        model = AddressLink
        fields = ["id", "institution", "address"]


class AddressLinkCustomerSerializer(serializers.ModelSerializer):
    """ address link serializer """
    address = AddressSerializer(many=False)

    class Meta:
        model = AddressLink
        fields = ["id", "address"]
