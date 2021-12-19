from rest_framework import serializers
from apps.company.models import Institution, Design, Analytics, SocialLinks, Requisites, WorkingHours, ExtraPhone


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


class AnalyticsSerializer(serializers.ModelSerializer):
    """ Analytics serializer """

    class Meta:
        model = Analytics
        exclude = ['institution']


class SocialLinksSerializer(serializers.ModelSerializer):
    """ Social links serializer """

    class Meta:
        model = SocialLinks
        exclude = ['institution']


class RequisitesSerializer(serializers.ModelSerializer):
    """ Requisites serializer """

    class Meta:
        model = Requisites
        exclude = ['institution']



class WorkingHoursSerializer(serializers.ModelSerializer):
    """ Working Hours serializer """

    class Meta:
        model = WorkingHours
        exclude = ['institution']


class ExtraPhoneSerializer(serializers.ModelSerializer):
    """ Extra Phone serializer """

    class Meta:
        model = ExtraPhone
        exclude = ['institution']

