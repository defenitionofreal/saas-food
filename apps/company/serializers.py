from rest_framework import serializers
from apps.company.models import Institution, Design, Analytics, SocialLinks, \
    Requisites, WorkingHours, ExtraPhone, Banner, MinCartCost


class InstitutionSerializer(serializers.ModelSerializer):
    """ Institution serializer """

    class Meta:
        model = Institution
        exclude = ['user']

    def get_logo_url(self, institution):
        request = self.context.get('request')
        logo_url = institution.logo.url
        return request.build_absolute_uri(logo_url)


class DesignSerializer(serializers.ModelSerializer):
    """ Design serializer """

    def get_institution(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Design
        fields = ['id', 'institution', 'color']
        #exclude = ['institution']


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


class BannerSerializer(serializers.ModelSerializer):
    """ Banner serializer """

    class Meta:
        model = Banner
        exclude = ['institution']


class MinCartCostSerializer(serializers.ModelSerializer):
    """ Min Cart Cost serializer """

    class Meta:
        model = MinCartCost
        exclude = ['institution']
