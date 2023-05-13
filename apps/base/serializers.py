from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


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


class LoginObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = str(user.phone) # ?
        token['email'] = user.email
        return token


class AuthSendCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)


class AuthPhoneSerializer(AuthSendCodeSerializer):
    code = serializers.CharField(required=True)

    # def create(self, validated_data):
    #     raise AttributeError("Serializer can't create instance")
    #
    # def update(self, instance, validated_data):
    #     raise AttributeError("Serializer can't update instance")
