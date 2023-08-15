from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.base.models import WeekDay

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name',
                  'phone', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'middle_name', 'last_name',
            'email', 'phone', 'image', 'password', 'is_customer',
            'is_organization', 'is_email_verified', 'is_sms_verified'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            # 'phone': {'required': False}
        }

    def get_fields(self):
        fields = super().get_fields()
        # Remove password field during updates
        if self.instance:
            del fields['password']
        return fields

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        email = validated_data.get('email')
        phone = validated_data.get('phone')

        if email and email != instance.email:
            instance.is_email_verified = False

        if phone and phone != instance.phone:
            instance.is_sms_verified = False

        instance = super().update(instance, validated_data)
        return instance


class WeekDaySerializer(serializers.ModelSerializer):
    """ Week Day serializer """

    class Meta:
        model = WeekDay
        fields = "__all__"


class SessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(read_only=True)
    max_age = serializers.CharField(read_only=True)
