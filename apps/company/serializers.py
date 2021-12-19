from rest_framework import serializers
from apps.company.models import Institution, Design


class InstitutionSerializer(serializers.ModelSerializer):
    """ Institution serializer """

    class Meta:
        model = Institution
        exclude = ['user']


class DesignSerializer(serializers.ModelSerializer):
    """ Design serializer """

    class Meta:
        model = Design
        exclude = ['institution']

