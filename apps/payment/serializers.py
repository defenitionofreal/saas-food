from rest_framework import serializers
from apps.payment.models import YooMoney, PaymentTypeInstitution


class YooMoneySerializer(serializers.ModelSerializer):
    """ YooMoney serializer """

    class Meta:
        model = YooMoney
        exclude = ['user']


class PaymentTypeInstitutionSerializer(serializers.ModelSerializer):

    institution = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTypeInstitution
        fields = '__all__'

    def get_institution(self, instance):
        return [affiliate.title for affiliate in instance.institution.all()]
