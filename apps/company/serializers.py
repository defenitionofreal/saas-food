from rest_framework import serializers
from apps.company.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    """ Institution serializer """

    class Meta:
        model = Institution
        exclude = ['user']

