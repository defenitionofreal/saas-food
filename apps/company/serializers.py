from rest_framework import serializers, exceptions
from apps.company.models import (
    Institution, Design, Analytics, SocialLinks, Requisites, WorkHours,
    ExtraPhone, Banner, MinCartCost, OrganizationTimeZone
)
from apps.company.services.validate_institution import validate_institution_list


class TimeZoneListSerializer(serializers.Serializer):
    timezone = serializers.ListSerializer(child=serializers.CharField())


class OrganizationTimeZoneSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OrganizationTimeZone
        fields = "__all__"

    def validate_institutions_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = OrganizationTimeZone.objects.filter(user=user)
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

    def save(self, **kwargs):
        user = self.context["request"].user
        kwargs["user"] = user
        return super().save(**kwargs)



class DesignSerializer(serializers.ModelSerializer):
    """ Design serializer """

    class Meta:
        model = Design
        fields = "__all__"

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.context["request"].user)
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


class WorkHoursSerializer(serializers.ModelSerializer):
    """ Work Hours serializer """

    class Meta:
        model = WorkHours
        fields = "__all__"
        extra_kwargs = {'user': {'required': False}}

    def get_institutions(self):
        qs = Institution.objects.filter(user=self.context["request"].user)
        serializer = InstitutionSerializer(instance=qs, many=True)
        return serializer.data

    def validate_data(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        institutions_data = validated_data.get("institutions")
        weekdays_data = validated_data.get("weekdays")
        institution_qs = Institution.objects.filter(user=user)
        instance_qs = WorkHours.objects.filter(user=user)

        validate_institution_list(
            institutions_data, institution_qs, instance_qs
        )
        # week day validation
        existing_work_hours = WorkHours.objects.filter(
            institutions__in=institutions_data,
            weekdays__in=weekdays_data,
            user=user
        )
        if existing_work_hours.exists():
            raise exceptions.ValidationError(
                {"detail": "Week days already relates with affiliate."}
            )

    def create(self, validated_data):
        self.validate_data(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.institutions.clear()
        instance.weekdays.clear()
        self.validate_data(validated_data)
        return super().update(instance, validated_data)


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
