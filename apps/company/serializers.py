from rest_framework import serializers
from apps.company.models import (
    Institution, Design, Analytics, SocialLinks,
    Requisites, WorkingHours, ExtraPhone, Banner, MinCartCost
)
from apps.company.services.validate_institution import validate_institution_list


class DesignSerializer(serializers.ModelSerializer):
    """ Design serializer """

    class Meta:
        model = Design
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Design.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=True
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class AnalyticsSerializer(serializers.ModelSerializer):
    """ Analytics serializer """

    class Meta:
        model = Analytics
        fields = "__all__"

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        institutions_data = validated_data.get("institution")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Analytics.objects.filter(institution=institutions_data)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=True
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)


class SocialLinksSerializer(serializers.ModelSerializer):
    """ Social links serializer """

    class Meta:
        model = SocialLinks
        fields = "__all__"

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        institutions_data = validated_data.get("institution")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = SocialLinks.objects.filter(institution=institutions_data)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=True
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)


class RequisitesSerializer(serializers.ModelSerializer):
    """ Requisites serializer """

    class Meta:
        model = Requisites
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Requisites.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=True
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class WorkingHoursSerializer(serializers.ModelSerializer):
    """ Working Hours serializer """

    class Meta:
        model = WorkingHours
        exclude = ['institution']


class ExtraPhoneSerializer(serializers.ModelSerializer):
    """ Extra Phone serializer """

    class Meta:
        model = ExtraPhone
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = ExtraPhone.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class BannerSerializer(serializers.ModelSerializer):
    """ Banner serializer """

    class Meta:
        model = Banner
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = Banner.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class MinCartCostSerializer(serializers.ModelSerializer):
    """ Min Cart Cost serializer """

    class Meta:
        model = MinCartCost
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = MinCartCost.objects.filter(user=user)
        validate_institution_list(
            institutions_data, institution_qs, instance_qs, check_duplicate=True
        )

    def create(self, validated_data):
        self.validate_institutions_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        self.validate_institutions_data(validated_data)
        return super().update(instance, validated_data)


class InstitutionSerializer(serializers.ModelSerializer):
    """ Institution serializer """
    other_phone = ExtraPhoneSerializer(read_only=True, many=True)

    class Meta:
        model = Institution
        exclude = ['user']

    def get_logo_url(self, institution):
        request = self.context.get('request')
        logo_url = institution.logo.url
        return request.build_absolute_uri(logo_url)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BasicInstitutionSerializer(serializers.ModelSerializer):
    """ basic affiliate serializer for nested serializers"""

    class Meta:
        model = Institution
        fields = ["id", "title", "domain"]
