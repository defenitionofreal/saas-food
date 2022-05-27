from rest_framework import serializers
from apps.location.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """ address serializer """

    class Meta:
        model = Address
        fields = '__all__'
