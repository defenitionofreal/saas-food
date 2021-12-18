from rest_framework import serializers
from apps.location.models import address, city, region, street


class AddressSerializer(serializers.ModelSerializer):
    """ address serializer """

    class Meta:
        model = address
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """ city serializer """

    class Meta:
        model = city
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    """ region serializer """

    class Meta:
        model = region
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    """ street serializer """

    class Meta:
        model = street
        fields = '__all__'
