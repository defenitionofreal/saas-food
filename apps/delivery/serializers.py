from rest_framework import serializers
from apps.delivery.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    """ Delivery serializer """

    class Meta:
        model = Delivery
        exclude = ['institution']
