from rest_framework import serializers
from apps.payment.models import YooMoney


class YooMoneySerializer(serializers.ModelSerializer):
    """ YooMoney serializer """

    class Meta:
        model = YooMoney
        exclude = ['user']
