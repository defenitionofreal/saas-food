from rest_framework import serializers

from apps.company.models import Institution
from apps.company.serializers import BasicInstitutionSerializer
from apps.company.services.validate_institution import validate_institution_list
from apps.payment.models import YooMoney, PaymentTypeInstitution


class YooMoneySerializer(serializers.ModelSerializer):
    """ YooMoney serializer """

    class Meta:
        model = YooMoney
        exclude = ['user']


class PaymentTypeInstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTypeInstitution
        fields = '__all__'
        read_only_fields = ["user"]

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = PaymentTypeInstitution.objects.filter(user=user)
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
